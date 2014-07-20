{
    'example': {url: "http://shermanpay.com",
              port: 8080,
              service_root: "/uw_schedule",
              services: {"/find_user": {params: [['user_name'],
                                                 ["shermpay"]],
                                        method: 'GET'},
                     }
          }
}
