create_ex04_movies_query = '''
            CREATE TABLE IF NOT EXISTS ex04sql_movies (
                episode_nb SERIAL PRIMARY KEY,
                title VARCHAR(64) UNIQUE NOT NULL,
                opening_crawl TEXT,
                director VARCHAR(32) NOT NULL,
                producer VARCHAR(128) NOT NULL,
                release_date DATE NOT NULL
            );
        '''


populate_ex04_movies_query = '''
                    INSERT INTO ex04sql_movies (episode_nb, title, director, producer, release_date)
                    VALUES (%s, %s, %s, %s, %s);
                '''
