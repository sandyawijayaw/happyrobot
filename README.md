# happyrobot
This code repository contains a web application I built using **Flask** with **three API endpoints** that are called in webhooks on my HappyRobot configuration that creates an AI assistant receiving inbound calls from carriers to book loads.

## ✅ What this App Does:

1. **`/verify-mc`**: Confirms a carrier's MC number by accessing the official FMCSA data.
2. **`/get-load`**: Retrieves the details of a load (e.g. origin, destination, rate) and returns a pitch the voice agent will say to the carrier.
3. **`/book-load`**: Records a load as "booked" when the carrier agrees to take it and saves it.

---

## ☁️ Backend:

- **Containerized on Docker:** The entire solution (the app, its settings and tools that allow it to run as expected) is packaged into a **Docker container** for easy sharing. Meaning it runs the same way no matter where it's deployed.
- **Deployed on AWS Elastic Beanstalk:** Our app is deployed on AWS EB by running my stored Docker Image on EC2, which are virtual machines in the cloud, so that the app can scale easily. Simply put, AWS EB sets up the servers
- **API Calls**: **`/verify-mc`** and **`/get-load`** are integrated into GET webhooks on HappyRobot because you're *getting* information, and **`/book-load`** is integrated into POST webhooks because you're *sending* information somewhere (in this case our booked_loads.json file).

---

## 🛠️ How to Reproduce This Project

#### 🪜 1. Setup Your Environment

* Install Docker.
* Install the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).

#### 🗂️ 2. Project Files

* `application.py` — The Flask app code.
* `fmcsa_utils.py` — Code to check the FMCSA API -- theoretically can combine this into app code as well.
* `loads_db.json` — My mock load dataset. Just created 2 records for now.
* `booked_loads.json` — Where booked loads get saved.
* `.env` — Stored my FMCSA API key like this:
  `FMCSA_API_KEY=your_api_key_here`
* `Dockerfile` — Tells Docker how to build your app.
* `requirements.txt` — Lists Python packages your app needs.

#### 🐳 3. Build Docker Image

```bash
docker build -t happyrobot-api .
```

#### ☁️ 4. Setup AWS Elastic Beanstalk

* Create an AWS account.
* Install & configure the AWS CLI:

```bash
aws configure
```

Enter your AWS credentials, default region, and output format.

* Initialize your Elastic Beanstalk app:

```bash
eb init -p docker happyrobot-app --region us-west-2
```

* Create and deploy:

```bash
eb create happyrobot-env
eb deploy
```

#### 🌐 5. Access Your Live App

After deployment, you'll get a public URL like:

```
http://happyrobot-env.eba-xyz.us-west-2.elasticbeanstalk.com
```

This is the URL used in HappyRobot webhook nodes.

#### 🔁  6. Sanity Check
**GET MC verification:** Set URL in HappyRobot as http://happyrobot-api-dev.us-west-2.elasticbeanstalk.com/verify-mc and mc_number as a query parameter 
- http://happyrobot-api-dev.us-west-2.elasticbeanstalk.com/verify-mc?mc_number=123456 will return the carrier details for the carrier with MC number 123456, including the argument "allowedToOperate" which is the main one I look at to verify a carrier's identity. 

**GET load information:** Set URL in HappyRobot as http://happyrobot-api-dev.us-west-2.elasticbeanstalk.com/get-load and load_id as a query parameter
- http://happyrobot-api-dev.us-west-2.elasticbeanstalk.com/get-load?load_id=123 will return the carrier details for the load with load ID 123, including all the details into a pitch. 

**POST booked load:** Set URL in HappyRobot as http://happyrobot-api-dev.us-west-2.elasticbeanstalk.com/book-load and add what information you want to send as a root field in the body so that running:
```bash
curl -X POST "http://happyrobot-api-dev.us-west-2.elasticbeanstalk.com/book-load" \
  -H "Content-Type: application/json" \
  -d '{"load_id": "load123", "carrier": "CarrierName", "details": "some details"}'
```
will return {"message":"Booking recorded","status":"success"} and add this booked load into to booked_loads.json file. 

---

## Quick guides

* Rebuild Docker image if testing locally:

```bash
docker build -t happyrobot-api .
```

* Redeploy to AWS:

```bash
eb deploy
```
