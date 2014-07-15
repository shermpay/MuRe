 {
     'test1': {'url': "http://shermanpay.com",
               'port': 8080,
               'service_root': "/uw_schedule",
               'services': {"/find_courses": [['user_name', "quarter"], 
                                              ["shermpay", "14au"],
                                              ["shermpay", "13au"]],
                            "/find_user": [['user_name'],
                                            ["shermpay"]]},
               'request_type': 'GET'}
}

