"""
PhoneBook — TSIS 1
Requires: psycopg2, database.ini in the same folder, setup.sql already run in psql.
"""

import psycopg2
import csv
import json
from config import load_config


def get_conn():
    return psycopg2.connect(**load_config())


def print_row(row):
    """Print one contact. Row = (id, username, email, birthday, group, phones)"""
    cid, name, email, bday, grp, phones = row
    print(f"  [{cid}] {name}"
          f"  | email: {email or '-'}"
          f"  | birthday: {bday or '-'}"
          f"  | group: {grp or '-'}"
          f"  | phones: {phones or '-'}")


# ── 1. CHECK SETUP ───────────────────────────────────────────────────────────

def check_setup():
    """Verify that tables and procedures exist in the database."""
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT table_name FROM information_schema.tables
                    WHERE table_schema='public'
                      AND table_name IN ('phonebook','phones','groups')
                    ORDER BY table_name;
                """)
                tables = [r[0] for r in cur.fetchall()]

                cur.execute("""
                    SELECT routine_name FROM information_schema.routines
                    WHERE routine_schema='public'
                      AND routine_name IN (
                          'upsert_u','loophz','del_user',
                          'add_phone','move_to_group',
                          'pagination','search_contacts')
                    ORDER BY routine_name;
                """)
                routines = [r[0] for r in cur.fetchall()]

        need_tables   = ['groups', 'phonebook', 'phones']
        need_routines = ['add_phone','del_user','loophz','move_to_group',
                         'pagination','search_contacts','upsert_u']

        missing_t = [t for t in need_tables   if t not in tables]
        missing_r = [r for r in need_routines if r not in routines]

        if not missing_t and not missing_r:
            print("OK — all tables and procedures are ready.")
        else:
            if missing_t:
                print(f"MISSING tables:     {missing_t}")
            if missing_r:
                print(f"MISSING procedures: {missing_r}")
            print("\nFix: open psql and run:")
            print(r"  \c phonebook")
            print(r"  \i setup.sql")

    except Exception as e:
        print(f"Connection error: {e}")
        print("Check your database.ini credentials.")


# ── 2. UPSERT  (from Practice 8) ─────────────────────────────────────────────

def upsert_contact():
    """Add a contact + phone. If username exists, just adds the phone."""
    username = input("Username: ").strip()
    phone    = input("Phone: ").strip()
    ptype    = input("Phone type (home/work/mobile) [mobile]: ").strip() or "mobile"

    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL upsert_u(%s, %s, %s);", (username, phone, ptype))
            conn.commit()
        print(f"Done — '{username}' saved.")
    except Exception as e:
        print(f"Error: {e}")


# ── 3. BULK INSERT  (from Practice 8) ────────────────────────────────────────

def bulk_insert():
    """Insert many contacts at once. Invalid entries are skipped with a warning."""
    print("Usernames (space-separated): ", end="")
    usernames = input().split()
    print("Phones (same order):         ", end="")
    phones = input().split()

    if len(usernames) != len(phones):
        print("Count mismatch — aborting.")
        return

    try:
        with get_conn() as conn:
            conn.notices.clear()
            with conn.cursor() as cur:
                cur.execute("CALL loophz(%s, %s);", (usernames, phones))
            conn.commit()
            for n in conn.notices:
                print("WARNING:", n.strip())
        print("Bulk insert done.")
    except Exception as e:
        print(f"Error: {e}")


# ── 4. UPDATE  (from Practice 7) ─────────────────────────────────────────────

def update_contact():
    """Update username, email, or birthday of a contact."""
    print("Update:  1.Username  2.Email  3.Birthday")
    choice = input("Choice: ").strip()
    field_map = {"1": "username", "2": "email", "3": "birthday"}
    if choice not in field_map:
        print("Invalid.")
        return
    field    = field_map[choice]
    old_name = input("Current username: ").strip()
    new_val  = input(f"New {field}: ").strip()

    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                # field comes from our own dict — no SQL injection possible
                cur.execute(f"UPDATE phonebook SET {field}=%s WHERE username=%s",
                            (new_val, old_name))
                changed = cur.rowcount
            conn.commit()
        print(f"Updated." if changed else "No contact with that username.")
    except Exception as e:
        print(f"Error: {e}")


# ── 5. ADD PHONE  (new — calls add_phone procedure) ──────────────────────────

def add_phone():
    """Add an extra phone number to an existing contact."""
    name  = input("Username: ").strip()
    phone = input("New phone: ").strip()
    ptype = input("Type (home/work/mobile) [mobile]: ").strip() or "mobile"

    try:
        with get_conn() as conn:
            conn.notices.clear()
            with conn.cursor() as cur:
                cur.execute("CALL add_phone(%s, %s, %s);", (name, phone, ptype))
            conn.commit()
            for n in conn.notices:
                print(n.strip())
    except Exception as e:
        print(f"Error: {e}")


# ── 6. MOVE TO GROUP  (new — calls move_to_group procedure) ──────────────────

def move_to_group():
    """Move a contact to a group. Creates the group if it doesn't exist."""
    name  = input("Username: ").strip()
    group = input("Group name: ").strip()

    try:
        with get_conn() as conn:
            conn.notices.clear()
            with conn.cursor() as cur:
                cur.execute("CALL move_to_group(%s, %s);", (name, group))
            conn.commit()
            for n in conn.notices:
                print(n.strip())
    except Exception as e:
        print(f"Error: {e}")


# ── 7. QUERY  (from Practice 7 + sort) ───────────────────────────────────────

def query_contacts():
    """Search by name / phone / email with sorting."""
    print("Filter:  1.Name  2.Phone prefix  3.Email")
    mode = input("Choice: ").strip()
    print("Sort by: 1.Name  2.Birthday  3.Date added")
    sort = {"1":"c.username","2":"c.birthday","3":"c.created_at"}.get(
            input("Choice: ").strip(), "c.username")

    # Base query — same JOIN structure for all three modes
    base = f"""
        SELECT c.id, c.username, c.email, c.birthday, g.name,
               STRING_AGG(p.phone||' ('||COALESCE(p.type,'?')||')', ', ')
        FROM phonebook c
        LEFT JOIN groups g ON g.id = c.group_id
        LEFT JOIN phones p ON p.contact_id = c.id
        WHERE {{where}}
        GROUP BY c.id, c.username, c.email, c.birthday, g.name, c.created_at
        ORDER BY {sort}
    """
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                if mode == "1":
                    val = input("Name (or part): ").strip()
                    cur.execute(base.format(where="c.username ILIKE %s"),
                                (f"%{val}%",))
                elif mode == "2":
                    val = input("Phone prefix: ").strip()
                    cur.execute(base.format(where="p.phone LIKE %s"),
                                (f"{val}%",))
                elif mode == "3":
                    val = input("Email (or part): ").strip()
                    cur.execute(base.format(where="c.email ILIKE %s"),
                                (f"%{val}%",))
                else:
                    print("Invalid.")
                    return
                rows = cur.fetchall()

        if rows:
            for r in rows: print_row(r)
        else:
            print("No results.")
    except Exception as e:
        print(f"Error: {e}")


# ── 8. FILTER BY GROUP  (new) ─────────────────────────────────────────────────

def filter_by_group():
    """Show contacts from one group."""
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name FROM groups ORDER BY name;")
                groups = cur.fetchall()

        print("Groups:")
        for gid, gname in groups:
            print(f"  {gid}. {gname}")

        choice = input("Enter group name or id: ").strip()

        with get_conn() as conn:
            with conn.cursor() as cur:
                col = "g.id" if choice.isdigit() else "g.name"
                val = int(choice) if choice.isdigit() else choice
                cur.execute(f"""
                    SELECT c.id, c.username, c.email, c.birthday, g.name,
                           STRING_AGG(p.phone||' ('||COALESCE(p.type,'?')||')', ', ')
                    FROM phonebook c
                    JOIN groups g ON g.id = c.group_id
                    LEFT JOIN phones p ON p.contact_id = c.id
                    WHERE {col} = %s
                    GROUP BY c.id, c.username, c.email, c.birthday, g.name
                    ORDER BY c.username;
                """, (val,))
                rows = cur.fetchall()

        if rows:
            for r in rows: print_row(r)
        else:
            print("No contacts in that group.")
    except Exception as e:
        print(f"Error: {e}")


# ── 9. FULL SEARCH  (new — calls search_contacts function) ───────────────────

def full_search():
    """Search name + email + all phone numbers at once."""
    query = input("Search: ").strip()
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM search_contacts(%s);", (query,))
                rows = cur.fetchall()
        if rows:
            for r in rows: print_row(r)
        else:
            print("No results.")
    except Exception as e:
        print(f"Error: {e}")


# ── 10. PAGINATED BROWSE  (from Practice 8 + next/prev loop) ─────────────────

def paginated_browse():
    """Browse page by page. Commands: next / prev / quit"""
    page_size = 5
    page      = 0

    while True:
        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM pagination(%s,%s);",
                                (page_size, page * page_size))
                    rows = cur.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return

        if not rows and page == 0:
            print("No contacts in the database.")
            return

        print(f"\n--- Page {page+1} ---")
        for r in rows:
            print_row(r)
        if len(rows) < page_size:
            print("(last page)")

        cmd = input("next / prev / quit: ").strip().lower()
        if   cmd == "next": page += 1 if len(rows) == page_size else 0
        elif cmd == "prev": page = max(0, page - 1)
        elif cmd == "quit": break


# ── 11. DELETE  (from Practice 8) ────────────────────────────────────────────

def delete_contact():
    """Delete by username or phone number."""
    print("Delete by:  1.Username  2.Phone")
    choice = input("Choice: ").strip()
    if choice == "1":
        val = input("Username: ").strip()
    elif choice == "2":
        val = input("Phone: ").strip()
    else:
        print("Invalid.")
        return

    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL del_user(%s);", (val,))
            conn.commit()
        print("Deleted.")
    except Exception as e:
        print(f"Error: {e}")


# ── 12. CSV IMPORT  (from Practice 7, extended) ───────────────────────────────

def csv_import():
    """Import from CSV. Columns: username, phone, phone_type, email, birthday, group"""
    path = input("CSV path [contacts.csv]: ").strip() or "contacts.csv"

    try:
        with open(path, newline='', encoding='utf-8') as f:
            rows = list(csv.DictReader(f))
    except FileNotFoundError:
        print(f"File not found: {path}")
        return

    inserted = skipped = 0
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                for row in rows:
                    username = row.get('username','').strip()
                    if not username:
                        skipped += 1
                        continue

                    phone      = row.get('phone','').strip()
                    phone_type = row.get('phone_type','mobile').strip() or 'mobile'
                    email      = row.get('email','').strip() or None
                    birthday   = row.get('birthday','').strip() or None
                    group_name = row.get('group','').strip() or None

                    # resolve group_id
                    group_id = None
                    if group_name:
                        cur.execute(
                            "INSERT INTO groups(name) VALUES(%s) ON CONFLICT(name) DO NOTHING;",
                            (group_name,))
                        cur.execute("SELECT id FROM groups WHERE name=%s;", (group_name,))
                        res = cur.fetchone()
                        group_id = res[0] if res else None

                    # insert contact
                    cur.execute("""
                        INSERT INTO phonebook (username, email, birthday, group_id)
                        VALUES (%s,%s,%s,%s)
                        ON CONFLICT (username) DO NOTHING;
                    """, (username, email, birthday, group_id))

                    if cur.rowcount == 0:
                        skipped += 1
                    else:
                        inserted += 1

                    # insert phone
                    if phone:
                        cur.execute("SELECT id FROM phonebook WHERE username=%s;",
                                    (username,))
                        cid = cur.fetchone()
                        if cid:
                            cur.execute("""
                                INSERT INTO phones (contact_id, phone, type)
                                VALUES (%s,%s,%s) ON CONFLICT DO NOTHING;
                            """, (cid[0], phone, phone_type))

            conn.commit()
        print(f"CSV done — {inserted} inserted, {skipped} skipped.")
    except Exception as e:
        print(f"Error: {e}")


# ── 13. EXPORT JSON  (new) ────────────────────────────────────────────────────

def export_json():
    """Export all contacts to a JSON file."""
    path = input("Output file [contacts.json]: ").strip() or "contacts.json"
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT c.id, c.username, c.email, c.birthday::TEXT, g.name
                    FROM phonebook c
                    LEFT JOIN groups g ON g.id = c.group_id
                    ORDER BY c.username;
                """)
                rows = cur.fetchall()
                out = []
                for cid, name, email, bday, grp in rows:
                    cur.execute(
                        "SELECT phone, type FROM phones WHERE contact_id=%s ORDER BY id;",
                        (cid,))
                    phones = [{"phone": p, "type": t} for p, t in cur.fetchall()]
                    out.append({"username":name,"email":email,
                                "birthday":bday,"group":grp,"phones":phones})

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
        print(f"Exported {len(out)} contacts to '{path}'.")
    except Exception as e:
        print(f"Error: {e}")


# ── 14. IMPORT JSON  (new) ────────────────────────────────────────────────────

def import_json():
    """Import contacts from a JSON file. Asks skip/overwrite on duplicates."""
    path = input("JSON file [contacts.json]: ").strip() or "contacts.json"
    try:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("File not found.")
        return
    except json.JSONDecodeError as e:
        print(f"Bad JSON: {e}")
        return

    inserted = skipped = overwritten = 0
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                for c in data:
                    username = c.get("username","").strip()
                    if not username:
                        skipped += 1
                        continue
                    email    = c.get("email")    or None
                    birthday = c.get("birthday") or None
                    grp      = c.get("group")    or None
                    phones   = c.get("phones", [])

                    cur.execute("SELECT id FROM phonebook WHERE username=%s;",
                                (username,))
                    existing = cur.fetchone()

                    if existing:
                        ans = input(f"'{username}' exists. (s)kip / (o)verwrite? ").strip().lower()
                        if ans != "o":
                            skipped += 1
                            continue
                        cid = existing[0]
                        cur.execute(
                            "UPDATE phonebook SET email=%s, birthday=%s WHERE id=%s;",
                            (email, birthday, cid))
                        cur.execute("DELETE FROM phones WHERE contact_id=%s;", (cid,))
                        overwritten += 1
                    else:
                        group_id = None
                        if grp:
                            cur.execute(
                                "INSERT INTO groups(name) VALUES(%s) ON CONFLICT(name) DO NOTHING;",
                                (grp,))
                            cur.execute("SELECT id FROM groups WHERE name=%s;", (grp,))
                            r = cur.fetchone()
                            group_id = r[0] if r else None

                        cur.execute("""
                            INSERT INTO phonebook (username,email,birthday,group_id)
                            VALUES (%s,%s,%s,%s) RETURNING id;
                        """, (username, email, birthday, group_id))
                        cid = cur.fetchone()[0]
                        inserted += 1

                    for ph in phones:
                        cur.execute("""
                            INSERT INTO phones (contact_id,phone,type)
                            VALUES (%s,%s,%s) ON CONFLICT DO NOTHING;
                        """, (cid, ph.get("phone"), ph.get("type","mobile")))

            conn.commit()
        print(f"JSON done — {inserted} inserted, {overwritten} overwritten, {skipped} skipped.")
    except Exception as e:
        print(f"Error: {e}")


# ── MENU ──────────────────────────────────────────────────────────────────────

def main():
    actions = {
        1:  check_setup,
        2:  upsert_contact,
        3:  bulk_insert,
        4:  update_contact,
        5:  add_phone,
        6:  move_to_group,
        7:  query_contacts,
        8:  filter_by_group,
        9:  full_search,
        10: paginated_browse,
        11: delete_contact,
        12: csv_import,
        13: export_json,
        14: import_json,
    }

    while True:
        print("""
PhoneBook — TSIS 1
----------------------------------
 1.  Check setup
 2.  Upsert contact
 3.  Bulk insert
 4.  Update contact field
 5.  Add phone to contact
 6.  Move contact to group
 7.  Query (name/phone/email)
 8.  Filter by group
 9.  Full search
 10. Browse pages
 11. Delete contact
 12. Import CSV
 13. Export JSON
 14. Import JSON
  0. Exit
----------------------------------""")
        try:
            choice = int(input("Choice: ").strip())
        except ValueError:
            print("Enter a number.")
            continue

        if choice == 0:
            print("Bye!")
            break
        elif choice in actions:
            print()
            actions[choice]()
        else:
            print("Unknown option.")


if __name__ == "__main__":
    main()
