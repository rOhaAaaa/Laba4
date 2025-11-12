import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  vus: __ENV.VUS ? parseInt(__ENV.VUS) : 16,
  duration: __ENV.DURATION || '4m',
};

const TARGET = __ENV.TARGET;

if (!TARGET) {
  throw new Error('Please set TARGET environment variable, e.g.: http://18.199.154.139:8080/heavy?seconds=3&mode=cpu');
}

export default function () {
  http.get(TARGET);
  sleep(0.1); 
}
