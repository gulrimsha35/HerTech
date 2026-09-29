# HackData AI

**Turn plain English into privacy-safe test data.**

## Problem Statement

Developers often need realistic test data for applications, but creating connected datasets manually is slow and difficult. Real customer data should not be used for testing because it may contain sensitive information.

## Planned Solution

HackData AI will be an LLM-powered synthetic-data platform. A user will describe the data they need in plain English. The platform will convert the request into a structured Data Plan, generate connected synthetic relational data, validate relationships and business rules, preview the results, and export CSV and JSON files.

## Planned Relational Tables

- `customers`
- `restaurants`
- `menu_items`
- `orders`
- `order_items`

## Planned Relationships

- `customers.customer_id` → `orders.customer_id`
- `restaurants.restaurant_id` → `menu_items.restaurant_id`
- `restaurants.restaurant_id` → `orders.restaurant_id`
- `orders.order_id` → `order_items.order_id`
- `menu_items.menu_item_id` → `order_items.menu_item_id`

## Tech Stack

### Frontend
- React
- TypeScript
- Vite

### Backend
- Python
- FastAPI

### Data Generation
- Faker
- Pandas

### Platform Storage
- SQLite
- SQLAlchemy

### Export
- CSV ZIP
- JSON ZIP

### LLM
- Optional OpenAI-compatible provider
- Demo Mode works without an API key

## Planned Architecture

The planned flow is:

```text
User
  |
  v
React + TypeScript + Vite
  |
  v
FastAPI Backend
  |
  +--> Data Plan
  |
  +--> Synthetic Data Generator
  |      |
  |      +--> Faker
  |      +--> Pandas
  |
  +--> Validator
  |
  +--> Exporter
  |
  +--> SQLite + SQLAlchemy
  |
  v
CSV ZIP / JSON ZIP