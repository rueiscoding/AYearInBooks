import {config} from 'dotenv';

config({path: `.env.${process.env.NODE_ENV || 'development'}.local`});

export const {UPSTASH_REDIS_REST_URL, UPSTASH_REDIS_REST_TOKEN} = process.env;