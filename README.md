Students API Load Testing
---

The purpose of this repo is to execute [Students API](https://github.com/osu-mist/students-api) load test using [Locust](https://github.com/locustio/locust).

## Usage

  1. Install all dependencies via pip:

      ```
      $ pip install -r requirements.txt
      ```

  2. Copy [config-example.yaml](config-example.yaml) as `config.yaml`. Modify as necessary, being careful to avoid committing sensitive data.

  3. Run API locally (e.g. https://localhost:8080) then start locust with Locust file:

      ```
      $ locust -f locustfile.py --host=https://localhost:8080
      ```

      Once the Locust started, you should be able to open up a browser and access Locust’s web interface via http://localhost:8089.

## Testing environment

* testing commit: [9ab6cf6](https://github.com/osu-mist/students-api/tree/9ab6cf6)
* testing database: ODS DEV2
* testing period: 10 minutes
* testing cases: 1336 different OSU IDs
* load balancers: 1 local instance

## Report

The following report is generated with different amount of users and mounting rates within 10 minutes.

| Connection Pools | # of Users | Hatch Rate (users spawned/sec) | # of Requests | # of Fails | Failure Rate | Average (ms) | 90%ile (ms) | Max (ms) | PRS |
| ---------------- | ---------- | ------------------------------ | ------------- | ---------- | ------------ | ------------ | ----------- | -------- |---- |
| 4 | 500 | 10 | 109204 | 22 | 0% | 50 | 69 | 2109 | 189.3 |
| 4 | 500 | 50 | 120024 | 59 | 0% | 66 | 74 | 4703 | 192.2 |
| 4 | 500 | 100 | 115660 | 46 | 0% | 52 | 82 | 1628 | 193 |
| 4 | 700 | 100 | 159940 | 102 | 0% | 66 | 130 | 1959 | 246.5 |
| 12 | 700 | 100 | 145658 | 62 | 0% | 82 | 190 | 4702 | 263.9 |
| 20 | 700 | 100 | 144853 | 74 | 0% | 80 | 230 | 1899 | 255.1 |
| 4 | 1000 | 100 | 215072 | 458 | 0% | 154 | 420 | 3857 | 369.3 |
| 12 | 1000 | 100 | 224941 | 680 | 0% | 129 | 350 | 3962 | 377.2 |
| 20 | 1000 | 100 | 234865 | 375 | 0% | 111 | 340 | 6282 | 380.6 |


From the report, the average response times are pretty constant under all scenarios. Although the max response time can exceed 4-7 seconds sometimes, they are still very rare cases among all of the requests. Average response time and the ninetieth percentile response time were pretty fast for each test cases. Also, looks like 4 connection pools (default number for the API) should be enough for each load balancer; adding more connection pools won't cause a huge difference. There are a very few failure requests, but all of them are `ConnectionError` due to too many users at a time, and I think it's expected and acceptable for this amount.
