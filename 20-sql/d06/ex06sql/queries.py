create_ex06_movies_query = '''
            CREATE TABLE IF NOT EXISTS ex06sql_movies (
                episode_nb SERIAL PRIMARY KEY,
                title VARCHAR(64) UNIQUE NOT NULL,
                opening_crawl TEXT,
                director VARCHAR(32) NOT NULL,
                producer VARCHAR(128) NOT NULL,
                release_date DATE NOT NULL,
				created TIMESTAMP DEFAULT NOW(),
                updated TIMESTAMP DEFAULT NOW()
            );
        '''


trigger_function = '''
			CREATE OR REPLACE FUNCTION update_changetimestamp_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated = NOW();
                NEW.created = OLD.created;
                RETURN NEW;
            END;
            $$ LANGUAGE 'plpgsql';
        '''

trigger = '''
			CREATE TRIGGER update_films_changetimestamp
            BEFORE UPDATE ON ex06sql_movies
            FOR EACH ROW
            EXECUTE PROCEDURE update_changetimestamp_column();
        '''


populate_ex06_movies_query = '''
                    INSERT INTO ex06sql_movies (episode_nb, title, director, producer, release_date)
                    VALUES (%s, %s, %s, %s, %s);
                '''
