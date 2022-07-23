
class GlobalXpath():
    update_btn = "/html/body/div[1]/main/div[1]/div/div/div/div[4]/button"
    metric_view = "/html/body/div[1]/main/div[1]/div/nav/ul/li[2]/a"
    result_view = "/html/body/div[1]/main/div[1]/div/nav/ul/li[1]/a"

class BreakdownXpath():

    # Net production
    netprod_base = "/html/body/div[1]/main/div[2]/section[1]/div[1]/div[1]/div/div/div[2]/h3"
    netprod_brk = "/html/body/div[1]/main/div[2]/section[1]/div[1]/div[1]/div/div/div[3]/a/ja-"
    netprod_brktotal = "/html/body/div[1]/main/div[2]/section[1]/div[1]/div[1]/div/div/div[3]/div/div/div/div[2]/div[2]/table/tr/td[3]/span"
    netprod_brkclose = "/html/body/div[1]/main/div[2]/section[1]/div[1]/div[1]/div/div/div[3]/div/div/div/div[1]/button"

    # Gross production
    grossprod_base = "/html/body/div[1]/main/div[2]/section[1]/div[1]/div[2]/div/div/div[2]/h3"
    grossprod_brk = "/html/body/div[1]/main/div[2]/section[1]/div[1]/div[2]/div/div/div[3]/a/ja-"
    grossprod_brktotal = "/html/body/div[1]/main/div[2]/section[1]/div[1]/div[2]/div/div/div[3]/div/div/div/div[2]/div[2]/table/tr/td[3]/span"
    grossprod_brkclose = "/html/body/div[1]/main/div[2]/section[1]/div[1]/div[2]/div/div/div[3]/div/div/div/div[1]/button"

    # Collection
    collection_base = "/html/body/div[1]/main/div[2]/section[1]/div[1]/div[3]/div/div/div[2]/h3"
    collection_brk = "/html/body/div[1]/main/div[2]/section[1]/div[1]/div[3]/div/div/div[3]/a/ja-"
    collection_brktotal = "/html/body/div[1]/main/div[2]/section[1]/div[1]/div[3]/div/div/div[3]/div/div/div/div[2]/div[2]/table/tr/td[3]/span"
    collection_brkclose = "/html/body/div[1]/main/div[2]/section[1]/div[1]/div[3]/div/div/div[3]/div/div/div/div[1]/button"

    # Adjustment
    adjustment_base = "/html/body/div[1]/main/div[2]/section[1]/div[1]/div[4]/div/div/div[2]/h3"
    adjustment_brk = "/html/body/div[1]/main/div[2]/section[1]/div[1]/div[4]/div/div/div[3]/a/ja-"
    adjustment_brktotal = "/html/body/div[1]/main/div[2]/section[1]/div[1]/div[4]/div/div/div[3]/div/div/div/div[2]/div[2]/table/tr/td[3]/span"
    adjustment_brkclose = "/html/body/div[1]/main/div[2]/section[1]/div[1]/div[4]/div/div/div[3]/div/div/div/div[1]/button"

    # --Patient Data

    # New Patient Visits
    nvs_base = "/html/body/div[1]/main/div[2]/section[2]/div/div[1]/div/div[1]/div/div/div[2]/h3"
    nvs_brk = "/html/body/div[1]/main/div[2]/section[2]/div/div[1]/div/div[1]/div/div/div[3]/a/ja-"
    nvs_brktotal = "//html/body/div[1]/main/div[2]/section[2]/div/div[1]/div/div[1]/div/div/div[3]/div/div/div/div[2]/div[2]/table/tbody/tr/td[1][@role='cell']"
    nvs_brkclose = "/html/body/div[1]/main/div[2]/section[2]/div/div[1]/div/div[1]/div/div/div[3]/div/div/div/div[1]/button"

    # Existing Patient Visits
    evs_base = "/html/body/div[1]/main/div[2]/section[2]/div/div[1]/div/div[2]/div/div/div[2]/h3"
    evs_brk = "/html/body/div[1]/main/div[2]/section[2]/div/div[1]/div/div[2]/div/div/div[3]/a/ja-"
    evs_brktotal = "/html/body/div[1]/main/div[2]/section[2]/div/div[1]/div/div[2]/div/div/div[3]/div/div/div/div[2]/div[2]/table/tr/td[5]/span"
    evs_brkclose = "/html/body/div[1]/main/div[2]/section[2]/div/div[1]/div/div[2]/div/div/div[3]/div/div/div/div[1]/button"

    financial_dataxpath = {"net_prod": [netprod_base, netprod_brk, netprod_brktotal, netprod_brkclose],
                           "gross_prod": [grossprod_base, grossprod_brk, grossprod_brktotal, grossprod_brkclose],
                           "adjustment": [adjustment_base, adjustment_brk, adjustment_brktotal, adjustment_brkclose],
                           "collection": [collection_base, collection_brk, collection_brktotal, collection_brkclose],
                           "newpatient_visit": [nvs_base, nvs_brk, nvs_brktotal, nvs_brkclose],
                           "existingpatient_visit": [evs_base, evs_brk, evs_brktotal, evs_brkclose]
    }

class ProductionTest():
    netprod_base = "/html/body/div[1]/main/div[2]/section[1]/div[1]/div[1]/div/div/div[2]/h3"
    providers_data = "/html/body/div[1]/main/div[2]/section[3]/div[1]/div/div[2]/div[1]/h3"
    table_total = "/html/body/div[1]/main/div[2]/section[3]/div[2]/div/div[2]/div/table/tr[2]/td[3]/strong"
    payor_score = "/html/body/div[1]/main/div[2]/section[3]/div/div[2]/div/div/table/tr/td[2]/strong"

    production_testxpath = {
                            "providers_data": [providers_data],
                            "table_total": [table_total],
                            "payor_score": [payor_score]
    }

class ServiceTest():
    service_code = "/html/body/div[1]/main/div[2]/section[4]/div/div[2]/div/div/table/tbody/tr/td[3]"
    search_input = "/html/body/div[1]/main/div[2]/section[4]/div/div[1]/div[2]/div[1]/input"
    search_code = "/html/body/div[1]/main/div[2]/section[4]/div/div[2]/div/div/table/tbody/tr/td[3]"
    service_type = "/html/body/div[1]/main/div[2]/section[4]/div/div[2]/div/div/table/tbody/tr/td[4]"
    service_provider = "/html/body/div[1]/main/div[2]/section[4]/div/div[2]/div/div/table/tbody/tr/td[2]"
    service_count = "/html/body/div[1]/main/div[2]/section[4]/div/div[2]/div/div/table/tbody/tr/td[5]/span/span[1]/span"
    count_brktotal = "/html/body/div[1]/main/div[3]/div/div/div/div[2]/section/div/div/div[2]/div/div[1]/table/tr/td[5]/strong/span"
    brk_close = "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div/button"


class BusinessTest():
    lineof_business = "//html/body/div[1]/main/div[1]/div/div/div/div[3]/div/button[not(@disabled) and @class='w-full py-2 pl-2 pr-6 text-xs text-left truncate border border-gray-700 dark:border-gray-800 rounded-sm bg-select dark:bg-select focus:outline-none focus:border-ja-green-200 h-9 bg-white dark:bg-gray-800 dark:text-white']"
    business_options = "/html/body/div[1]/main/div[1]/div/div/div/div[3]/div/div/div[2]/ul/li"
    clear_btn = "/html/body/div[1]/main/div[1]/div/div/div/div[3]/div/div/div[2]/div[1]/div/button[2]"
    provider_name = "/html/body/div[1]/main/div[2]/section[3]/div[2]/div/div[2]/div/table/tbody/tr/td[1]/span"
    business_brk = "/html/body/div[1]/main/div[2]/section[3]/div[2]/div/div[2]/div/table/tbody/tr/td[1]/span/span/a"
    speciality = "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/h5"
    close_btn = "/html/body/div[1]/main/div[3]/div/div/div/div[2]/div[1]/div[1]/button"

