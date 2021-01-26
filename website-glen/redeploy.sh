#!/bin/sh
cd Website_Glen/website-glen/
npm run build
systemctl reload nginx
systemctl daemon-reload
systemctl restart prodoplot