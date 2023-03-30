# fal-serverless Example Project with dbt

This is an example project for running [fal-serverlesss](https://docs.fal.ai/fal-serverless/quickstart) with dbt using the dbt-fal adapter. We will run a sentiment analysis model on some fake Zendesk data by building and running a Python model on fal-serverless on a GPU machine.

## 1. Pull the example repo
`git clone git@github.com:fal-ai/dbt-fal-serverless-demo.git`

## 2. Install fal-serverless and dbt-fal
`pip install fal-serverless dbt-fal[snowflake]`

## 3. Authenticate to fal-serverless
`fal-serverless auth login`

Follow the link that's generated and login using GitHub. Come back to the shell, when ready. (Reach out to the fal team for access if you don't already have it)

## 4. Generate keys to access fal-serverless
`fal-serverless key generate`

This will print a message containing values for KEY_ID and KEY_SECRET. We will need these for setting up the dbt profile.

## 5. Update your dbt profiles.yml
In order to run your Python models in fal-serverless, you should update the profiles.yml to include the newly generated credentials. Here's an example of how it should look like:

```yaml
fal_profile:
  target: fal_serverless
  outputs:
    fal_serverless:
      type: fal
      db_profile: db
      host: <ask the fal team>
      key_secret: MY_KEY_SECRET_VALUE
      key_id: MY_KEY_ID_VALUE
    db:
      type: snowflake
      username: USERNAME
      password: PASSWORD
```

That's it. Doing a dbt run against this profile will execute your Python models in fal-serverless.

## 6. Run dbt
`dbt seed` will create the seed data.
`dbt run` will run the SQL model and then run the Python model on fal Serverless on a GPU machine.
