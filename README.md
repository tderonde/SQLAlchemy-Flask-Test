# 10-SQLAlchemy


## Climate Analysis and Exploration

Climate analysis and data exploration of Hawaii climate database. Analysis completed using Python, SQLAlchemy ORM queries, Pandas, and Matplotlib.

### Precipitation Analysis

* Plot of most recent 12 months of Hawaii precipitation data

* Printed summary statistics for the precipitation data.

### Station Analysis

* Identified the most active stations (i.e., station with the most measurements) and calculated the lowest, highest, and average temperature.

* Plot of thte most recent 12 months of temperature observation data (TOBS) for this station as histogram

- - -

## Climate App

Flask API

### Routes

* `/`

  * Home page.

  * Lists all routes that are available.

* `/api/v1.0/precipitation`

  * Return the JSON list of precipiation by date

* `/api/v1.0/stations`

  * Return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`

  * Return a JSON list of temperature observations (TOBS) for the most recent year for the most active station

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range (inclusive).


- - -

### Temperature Analysis 

* Identify the average temperature in June vs December

* Use t-test to determine whether difference in the means is statistically significant
