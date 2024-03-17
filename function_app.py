import logging
import datetime
import azure.functions as func

app = func.FunctionApp()

@app.timer_trigger(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    current_time = datetime.datetime.now()
    logging.info(current_time)
    logging.info('Python timer trigger function executed.')
