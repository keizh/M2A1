import http from 'k6/http'
import { check, sleep } from 'k6'

export const options = {
    stages: [
        { duration: '5s', target: 100 },
        { duration: '15s', target: 100 },
        { duration: '5s', target: 0 }
    ]
}

export default function () {
    const targetUrl = 'http://localhost:8000/url/redirect?short_code=12i0T1c2';

    const res = http.get(targetUrl, { redirects: 0 })

    check(res, {
        'succesfull redirect': (r) => r.status == 307,
    })

    sleep(0.05)
}