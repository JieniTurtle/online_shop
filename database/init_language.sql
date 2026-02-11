-- CREATE TABLE LANGUAGE (
--     LANGUAGE_CODE VARCHAR(10) PRIMARY KEY,
--     NAME VARCHAR(20) NOT NULL
-- );

-- ALTER TABLE language 
-- ADD CONSTRAINT check_language_code
-- CHECK (LANGUAGE_CODE IN ('zh-CN', 'en-US'));

-- INSERT INTO LANGUAGE (LANGUAGE_CODE, NAME) VALUES
-- ('zh-CN', '简体中文'),
-- ('en-US', 'English');

SELECT * FROM "language" 