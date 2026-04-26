-- ============================================================
--  setup.sql
--  Run this ONE time to build the entire database.
--  It drops everything first so it is safe to re-run.
-- ============================================================

-- Drop in reverse dependency order
DROP FUNCTION  IF EXISTS search_contacts(text)           CASCADE;
DROP FUNCTION  IF EXISTS pagination(int, int)            CASCADE;
DROP FUNCTION  IF EXISTS records(text)                   CASCADE;
DROP PROCEDURE IF EXISTS move_to_group(varchar, varchar) CASCADE;
DROP PROCEDURE IF EXISTS add_phone(varchar, varchar, varchar) CASCADE;
DROP PROCEDURE IF EXISTS del_user(varchar)               CASCADE;
DROP PROCEDURE IF EXISTS loophz(varchar[], varchar[])    CASCADE;
DROP PROCEDURE IF EXISTS upsert_u(varchar, varchar, varchar) CASCADE;
DROP PROCEDURE IF EXISTS upsert_u(varchar, varchar)      CASCADE;
DROP TABLE IF EXISTS phones    CASCADE;
DROP TABLE IF EXISTS phonebook CASCADE;
DROP TABLE IF EXISTS contacts  CASCADE;
DROP TABLE IF EXISTS groups    CASCADE;

-- ── TABLES ──────────────────────────────────────────────────

CREATE TABLE groups (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO groups (name) VALUES ('Family'), ('Work'), ('Friend'), ('Other');

CREATE TABLE phonebook (
    id         SERIAL PRIMARY KEY,
    username   VARCHAR(50) UNIQUE NOT NULL,
    email      VARCHAR(100),
    birthday   DATE,
    group_id   INTEGER REFERENCES groups(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE phones (
    id         SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES phonebook(id) ON DELETE CASCADE,
    phone      VARCHAR(20) NOT NULL,
    type       VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
);

-- ── PROCEDURES ──────────────────────────────────────────────

-- Insert contact if not exists, then add the phone to phones table
CREATE PROCEDURE upsert_u(p_name VARCHAR, p_phone VARCHAR, p_type VARCHAR DEFAULT 'mobile')
LANGUAGE plpgsql AS $$
DECLARE v_id INT;
BEGIN
    INSERT INTO phonebook (username) VALUES (p_name)
    ON CONFLICT (username) DO NOTHING;

    SELECT id INTO v_id FROM phonebook WHERE username = p_name;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_id, p_phone, p_type)
    ON CONFLICT DO NOTHING;
END;
$$;

-- Bulk insert with validation: skips bad phones (letters) or bad names (digits)
CREATE PROCEDURE loophz(p_user VARCHAR[], p_phone VARCHAR[])
LANGUAGE plpgsql AS $$
BEGIN
    FOR i IN 1..array_length(p_user, 1) LOOP
        IF p_phone[i] ~ '[a-zA-Z_!@#$%]' THEN
            RAISE NOTICE 'Phone "%" is invalid — skipped.', p_phone[i];
        ELSIF p_user[i] ~ '[0-9]' THEN
            RAISE NOTICE 'Username "%" contains digits — skipped.', p_user[i];
        ELSE
            CALL upsert_u(p_user[i], p_phone[i]);
        END IF;
    END LOOP;
END;
$$;

-- Delete contact by username OR by phone number
CREATE PROCEDURE del_user(p VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook WHERE username = p;
    DELETE FROM phonebook WHERE id IN (
        SELECT contact_id FROM phones WHERE phone = p
    );
END;
$$;

-- Add a phone number to an existing contact
CREATE PROCEDURE add_phone(p_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE v_id INT;
BEGIN
    SELECT id INTO v_id FROM phonebook WHERE username = p_name;
    IF v_id IS NULL THEN
        RAISE NOTICE 'Contact "%" not found.', p_name;
        RETURN;
    END IF;
    INSERT INTO phones (contact_id, phone, type) VALUES (v_id, p_phone, p_type);
    RAISE NOTICE 'Phone added to "%".', p_name;
END;
$$;

-- Move contact to a group; creates the group if it does not exist
CREATE PROCEDURE move_to_group(p_name VARCHAR, p_group VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE v_gid INT; v_cid INT;
BEGIN
    INSERT INTO groups (name) VALUES (p_group) ON CONFLICT (name) DO NOTHING;
    SELECT id INTO v_gid FROM groups    WHERE name     = p_group;
    SELECT id INTO v_cid FROM phonebook WHERE username = p_name;
    IF v_cid IS NULL THEN
        RAISE NOTICE 'Contact "%" not found.', p_name;
        RETURN;
    END IF;
    UPDATE phonebook SET group_id = v_gid WHERE id = v_cid;
    RAISE NOTICE 'Moved "%" to group "%".', p_name, p_group;
END;
$$;

-- ── FUNCTIONS ───────────────────────────────────────────────

-- Paginated list of contacts (page-by-page browsing)
CREATE FUNCTION pagination(lim INT, offs INT)
RETURNS TABLE(
    out_id       INT,
    out_name     VARCHAR,
    out_email    VARCHAR,
    out_birthday DATE,
    out_group    VARCHAR,
    out_phones   TEXT
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
        SELECT c.id, c.username, c.email, c.birthday, g.name,
               STRING_AGG(p.phone || ' (' || COALESCE(p.type,'?') || ')', ', ')
        FROM phonebook c
        LEFT JOIN groups g ON g.id = c.group_id
        LEFT JOIN phones p ON p.contact_id = c.id
        GROUP BY c.id, c.username, c.email, c.birthday, g.name, c.created_at
        ORDER BY c.username
        LIMIT lim OFFSET offs;
END;
$$;

-- Search across name + email + all phone numbers at once
CREATE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    out_id       INT,
    out_name     VARCHAR,
    out_email    VARCHAR,
    out_birthday DATE,
    out_group    VARCHAR,
    out_phones   TEXT
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
        SELECT DISTINCT ON (c.id)
            c.id, c.username, c.email, c.birthday, g.name,
            (SELECT STRING_AGG(p2.phone || ' (' || COALESCE(p2.type,'?') || ')', ', ')
             FROM phones p2 WHERE p2.contact_id = c.id)
        FROM phonebook c
        LEFT JOIN groups g ON g.id = c.group_id
        LEFT JOIN phones p ON p.contact_id = c.id
        WHERE c.username ILIKE '%' || p_query || '%'
           OR c.email    ILIKE '%' || p_query || '%'
           OR p.phone    ILIKE '%' || p_query || '%'
        ORDER BY c.id;
END;
$$;

-- Done
SELECT 'Setup complete!' AS status;
