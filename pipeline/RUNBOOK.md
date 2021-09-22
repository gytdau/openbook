# Generating the DB

(TODO: Instructions on how to invoke the lambda)

Set an alarm on your phone in 30 minutes titlted `Change the DB back`. Then you can change the DB size from `db.t3.micro` which has a limit of 40 slots to `db.m6g.xlarge`, which should have a limit of about 1800. `db.m6g.xlarge` costs 30 cents per hour. Once done, please change the DB back, or else I will get charged a hell of a lot of money.

The slot limit is determined by `DBInstanceClassMemory/9531392` or `5000`, whichever is lower, where `DBInstanceClassMemory` is in bytes.

## Dashboards

[Lambda dashboard](https://eu-west-1.console.aws.amazon.com/cloudwatch/home?region=eu-west-1#metricsV2:graph=~(metrics~(~(~'AWS*2fLambda~'Errors~'FunctionName~'downloadBook~(id~'errors~color~'*23d13212))~(~'.~'Invocations~'.~'.~(id~'invocations))~(~(expression~'100*20-*20100*20*2a*20errors*20*2f*20MAX*28*5berrors*2c*20invocations*5d*29~label~'Success*20rate*20*28*25*29~id~'availability~yAxis~'right~region~'eu-west-1)))~period~10~region~'eu-west-1~title~'Error*20count*20and*20success*20rate*20*28*25*29~yAxis~(right~(max~100))~start~'-PT1H~end~'P0D~view~'timeSeries~stacked~false~stat~'Sum))

You should use pgAdmin 4 to connect to the DB to view the dashboard, which reports how the DB is doing