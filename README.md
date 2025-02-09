# Real-Time Insurance Bidding System

A modern, real-time platform connecting insurance carriers with consumers through live bidding.

## Overview

This system enables real-time bidding on insurance quotes, where carriers can compete to offer the best rates to consumers. The platform features live WebSocket updates, automated bid management, and a robust confirmation process.

## Architecture

- **Frontend**: Next.js with TypeScript and TailwindCSS
- **Backend**: Django with Django-Ninja
- **Database**: SQLite
- **Real-time**: WebSocket-based live updates
- **Background Tasks**: Async worker for bid processing

## Key Features

- Real-time quote requests and bidding
- Live bid updates via WebSockets
- Automated bid session management
- Two-phase confirmation process
- Rate-limiting and fair bidding rules
- Bid session restart capabilities

## Project Structure

- `frontend/`: Next.js application for consumer and carrier interfaces
- `backend/`: Django application with REST API and WebSocket server
- `docs/`: System documentation and API specifications

## Security

- JWT-based authentication
- Rate limiting for bid submissions
- Environment-based configuration
- OWASP security guidelines compliance
