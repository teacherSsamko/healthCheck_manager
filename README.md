# healthCheck_manager

pikavue health check manager

## systemd
```bash
[Unit]
Description=Run health check manager
After=multi-user.target

[Service]
User=root
Type=simple
WorkingDirectory = /home/ssamko/healthcheck_manager
ExecStart = /home/ssamko/healthcheck_manager/docker_task.sh
Restart = always
RestartSec = 1min

[Install]
WantedBy=multi-user.target
```

## deploy and run
1. `cd /home/ssamko/healthcheck_manager`
2. `git pull`
3. `sudo systemctl restart healthcheck`