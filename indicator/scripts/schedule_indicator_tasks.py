import logging
from indicator import controller


def run(indicator_type, category=None, context=None, years_number=None):
    years_number = years_number and int(years_number)
    logging.info((category, context, years_number))
    if indicator_type == "action":
        controller.schedule_directory_numbers_tasks(creator_id=1)

    elif indicator_type == "sciprod":
        controller.schedule_evolution_of_scientific_production_tasks(
            creator_id=1,
            years_range=controller.get_years_range(years_number or 10),
        )
    else:
        print("Expected action or sciprod")
    # journals_numbers(creator_id=1)
