import http from 'k6/http'
import { check, sleep } from 'k6'

export const options = {
    stages: [
        { duration: '5s', target: 5 },
        { duration: '5s', target: 10 },
        { duration: '5s', target: 0 }
    ]
}

export default function () {

    const targetUrl1 = 'http://localhost:8000/url/redirect?short_code=Oq7y9sY0aR';
    const targetUrl2 = 'http://localhost:8000/url/shorten';

    const res1 = http.get(targetUrl1, { redirects: 0 })
    check(res1, {
        'succesfull redirect': (r) => r.status == 307,
    })

    const randomString = Math.random().toString(36).substring(2);
    const res2 = http.post(targetUrl2, JSON.stringify({ long_url: `https://www.example.com/${randomString}` }), {
        headers: { 'Content-Type': 'application/json' },
    });

    check(res2, {
        'successfull Insert': (r) => r.status == 201
    })

    sleep(0.05)
}
