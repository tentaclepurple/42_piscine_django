create_ex08_planets = '''
            CREATE TABLE IF NOT EXISTS ex08sql_planets (
                id SERIAL PRIMARY KEY,
                name VARCHAR(64) UNIQUE NOT NULL,
                climate VARCHAR(128),
                diameter INTEGER,
                orbital_period INTEGER,
                population BIGINT,
                rotation_period INTEGER,
                surface_water REAL,
                terrain VARCHAR(128)
            );
        '''


create_ex08_people = '''
			CREATE TABLE IF NOT EXISTS ex08sql_people (
                id SERIAL PRIMARY KEY,
                name VARCHAR(64) UNIQUE NOT NULL,
                birth_year VARCHAR(32),
                gender VARCHAR(32),
                eye_color VARCHAR(32),
                hair_color VARCHAR(32),
                height INTEGER,
                mass REAL,
                homeworld VARCHAR(64) REFERENCES ex08sql_planets(name)
            );
        '''


get_people_with_homeworld_climate = '''
			SELECT ppl.name, ppl.homeworld, plnt.climate
            FROM ex08sql_people ppl
            JOIN ex08sql_planets plnt ON ppl.homeworld = plnt.name
            WHERE plnt.climate LIKE '%windy%'
            ORDER BY ppl.name;
		'''
