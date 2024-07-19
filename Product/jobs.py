from khayyam import JalaliDate
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from .models import Participants
from Calendar.models import Day
import logging

logger = logging.getLogger(__name__)


def refresh_teacher_day():
    try:
        # Get the current Jalali date
        current_jalali_date = JalaliDate.today()

        current_year = current_jalali_date.year
        current_month = current_jalali_date.month

        first_day = 1
        last_day = JalaliDate(current_year, current_month, 1).daysinmonth

        try:
            start_day = Day.objects.get(number=first_day, month__number=current_month,
                                        month__year__name=str(current_year))
            end_day = Day.objects.get(number=last_day, month__number=current_month, month__year__name=str(current_year))
        except Day.DoesNotExist:
            logger.error('Day objects for the start or end of the month do not exist.')
            return

        teacher_participants = Participants.objects.filter(user__is_teacher=True)

        for participant in teacher_participants:
            participant.startDay = start_day
            participant.endDay = end_day
            participant.save()
            logger.info(f'Updated participant {participant.id}')
    except Exception as e:
        logger.error(f"Error in refresh_teacher_day: {str(e)}")


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'default')

    try:
        # Register the job with a function reference as a string
        scheduler.add_job('Product.jobs.refresh_teacher_day', 'cron', month="*", day="1", id="refresh_teacher_day")
    except Exception as e:
        logger.error(f"Error adding job: {str(e)}")

    def job_listener(event):
        if hasattr(event, 'exception') and event.exception:
            logger.error(f'Job {event.job_id} failed with exception: {event.exception}')
        else:
            logger.info(f'Job {event.job_id} completed successfully')

    scheduler.add_listener(job_listener)

    scheduler.start()
    logger.info("Scheduler started ...")
