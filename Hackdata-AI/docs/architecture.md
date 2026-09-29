# Preliminary Architecture

HackData AI is planned as a small full-stack application.

```text
+---------------------------+
|          User             |
|  Plain-English request    |
+-------------+-------------+
              |
              v
+---------------------------+
| React + TypeScript + Vite |
|        Frontend           |
+-------------+-------------+
              |
              | HTTP API
              v
+---------------------------+
|      FastAPI Backend      |
+-------------+-------------+
              |
       +------+------+
       |             |
       v             v
+-------------+  +-------------+
| Data Plan   |  | Generator   |
| / Planner   |  | Faker/Pandas|
+-------------+  +------+------+
                         |
                         v
                  +-------------+
                  | Validator   |
                  | Keys/Rules  |
                  +------+------+
                         |
              +----------+----------+
              |                     |
              v                     v
       +-------------+       +-------------+
       | Exporter    |       | SQLite /    |
       | CSV / JSON  |       | SQLAlchemy  |
       +-------------+       +-------------+

Optional later:
FastAPI -> OpenAI-compatible LLM provider

Demo Mode:
The platform must work without an API key.