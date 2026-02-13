-- Drop the existing constraint (replace 'constraint_name' with the actual name)
ALTER TABLE language DROP CONSTRAINT IF EXISTS check_language_code;

-- Add the new constraint with 'cn' and 'en' values
ALTER TABLE language 
ADD CONSTRAINT check_language_code
CHECK (LANGUAGE_CODE IN ('cn', 'en'));

-- If you need to update existing records to match the new format:
-- UPDATE LANGUAGE SET LANGUAGE_CODE = 'cn' WHERE LANGUAGE_CODE = 'cn';
-- UPDATE LANGUAGE SET LANGUAGE_CODE = 'en' WHERE LANGUAGE_CODE = 'en-US';

-- Insert new values if they don't exist
INSERT INTO LANGUAGE (LANGUAGE_CODE, NAME) VALUES
('cn', '简体中文'),
('en', 'English')
ON CONFLICT (LANGUAGE_CODE) DO NOTHING;