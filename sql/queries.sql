SELECT id, full_name, email
FROM users
ORDER BY full_name;

SELECT id, name, is_final
FROM statuses
ORDER BY id;

SELECT
    a.id,
    a.title,
    a.description,
    a.created_at,
    u.full_name AS applicant,
    s.name AS status
FROM applications AS a
JOIN users AS u ON u.id = a.user_id
JOIN statuses AS s ON s.id = a.status_id
ORDER BY a.created_at DESC, a.id DESC;

SELECT
    a.id,
    a.title,
    u.full_name AS applicant,
    s.name AS status
FROM applications AS a
JOIN users AS u ON u.id = a.user_id
JOIN statuses AS s ON s.id = a.status_id
WHERE s.name = ?
ORDER BY a.created_at DESC;

SELECT
    a.id,
    a.title,
    u.full_name AS applicant,
    s.name AS status
FROM applications AS a
JOIN users AS u ON u.id = a.user_id
JOIN statuses AS s ON s.id = a.status_id
WHERE a.title LIKE ? OR a.description LIKE ? OR u.full_name LIKE ?
ORDER BY a.created_at DESC;

SELECT id, title, created_at
FROM applications
ORDER BY created_at DESC, id DESC
LIMIT ? OFFSET ?;

SELECT s.name AS status, COUNT(a.id) AS applications_count
FROM statuses AS s
LEFT JOIN applications AS a ON a.status_id = s.id
GROUP BY s.id, s.name
ORDER BY applications_count DESC, s.name;

SELECT COUNT(*) AS applications_count
FROM applications;

SELECT
    d.id,
    d.name,
    d.description,
    d.uploaded_at,
    a.title AS application_title
FROM documents AS d
JOIN applications AS a ON a.id = d.application_id
ORDER BY d.uploaded_at DESC, d.id DESC;

SELECT
    c.id,
    c.text,
    c.created_at,
    a.title AS application_title,
    u.full_name AS author
FROM comments AS c
JOIN applications AS a ON a.id = c.application_id
JOIN users AS u ON u.id = c.author_id
ORDER BY c.created_at DESC, c.id DESC;
