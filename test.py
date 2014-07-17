{
    'test1': {url: "http://shermanpay.com",
              port: 8080,
              service_root: "/uw_schedule",
              services: {"/find_courses": {params: [['user_name', "quarter"], 
                                                    ["shermpay", "14au"],
                                                    ["shermpay", "13au"]],
                                           method: 'GET'},
                         "/find_user": {params: [['user_name'],
                                                 ["shermpay"]],
                                        method: 'GET'},
                         }
              }
}
