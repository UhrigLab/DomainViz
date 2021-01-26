#!/bin/sh
npm run build
systemctl reload nginx
systemctl daemon-reload
systemctl restart prodoplot