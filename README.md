# M³-Bench · Project Website

Static project website for **M³-Bench: Multi-Modal, Multi-Hop, Multi-Threaded
Tool-Using MLLM Agent Benchmark**.

This folder is intended to be served with GitHub Pages from its own branch or
from the `main` branch using a `/blog` subpath.

## Layout

```
blog/
├── index.html
├── README.md
└── assets/
    ├── css/style.css
    ├── js/main.js
    └── img/
        ├── m3_logo.jpg
        ├── mcp_tools_per_server.png     # tools-per-server figure
        ├── metrics_mllm_step_eval.png   # step-level leaderboard figure
        ├── task_sample.jpg              # example shelf image from media/
        └── task_sample_2.jpg            # additional task image
```

The CSS + JS are shared with the sibling project **Open-SPARK** so the two
sites feel like part of the same umbrella.

## Preview locally

```bash
cd blog
python -m http.server 8000
# open http://localhost:8000
```

## Deployment

Point GitHub Pages at this folder, or push it to a dedicated `m3-bench-site`
repo, or mount it behind a reverse proxy — it's purely static HTML.
