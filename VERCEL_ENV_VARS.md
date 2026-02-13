# Vercel Environment Variables Configuration Guide

## Required Environment Variables (MUST SET)

These environment variables are **REQUIRED** for the application to work on Vercel:

### 1. `SECRET_KEY` ⚠️ CRITICAL
- **Description**: Django secret key for cryptographic signing
- **Required**: YES (application will fail to start without it)
- **How to generate**: Run `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` in your terminal
- **Example**: `django-insecure-abc123xyz...` (use a long random string)
- **Where to set**: Vercel Dashboard → Your Project → Settings → Environment Variables

### 2. `DEBUG`
- **Description**: Enable/disable debug mode
- **Required**: YES (for production)
- **Value**: `False` (must be the string "False", not boolean)
- **Note**: Setting this to `True` will disable SECRET_KEY validation, but should NEVER be used in production

### 3. `DATABASE_URL`
- **Description**: PostgreSQL database connection string
- **Required**: YES (unless you want to use SQLite, which is NOT recommended for production)
- **Format**: `postgresql://user:password@host:port/database`
- **Example**: `postgresql://user:pass@db.example.com:5432/visstesphere`
- **Where to get**: 
  - If using ElephantSQL: Copy from your database dashboard
  - If using Vercel Postgres: Vercel will provide this automatically
  - If using other providers: Check your database provider's documentation

## Optional but Recommended Environment Variables

### 4. `VERCEL_URL`
- **Description**: Automatically set by Vercel
- **Required**: NO (automatically provided by Vercel)
- **Note**: Don't manually set this - Vercel sets it automatically

### 5. `STRIPE_PUBLIC_KEY`
- **Description**: Stripe publishable key for payment processing
- **Required**: NO (only if using Stripe payments)
- **Where to get**: Stripe Dashboard → Developers → API Keys

### 6. `STRIPE_SECRET_KEY`
- **Description**: Stripe secret key for payment processing
- **Required**: NO (only if using Stripe payments)
- **Where to get**: Stripe Dashboard → Developers → API Keys

### 7. `STRIPE_WH_SECRET`
- **Description**: Stripe webhook secret for verifying webhook signatures
- **Required**: NO (only if using Stripe webhooks)
- **Where to get**: Stripe Dashboard → Developers → Webhooks → Select endpoint → Signing secret

## AWS S3 Configuration (Only if using AWS for static/media files)

### 8. `USE_AWS`
- **Description**: Enable AWS S3 storage
- **Required**: NO (only if using AWS S3)
- **Value**: `True` (string)

### 9. `AWS_ACCESS_KEY_ID`
- **Description**: AWS access key ID
- **Required**: NO (only if `USE_AWS=True`)
- **Where to get**: AWS IAM Console → Users → Your User → Security Credentials

### 10. `AWS_SECRET_ACCESS_KEY`
- **Description**: AWS secret access key
- **Required**: NO (only if `USE_AWS=True`)
- **Where to get**: AWS IAM Console → Users → Your User → Security Credentials

## Email Configuration (Only if using email functionality)

### 11. `EMAIL_HOST_USER`
- **Description**: Email address for sending emails
- **Required**: NO (only if using email features)
- **Example**: `your-email@gmail.com`

### 12. `EMAIL_HOST_PASSWORD`
- **Description**: Email password or app-specific password
- **Required**: NO (only if using email features)
- **Note**: For Gmail, use an App Password, not your regular password

## How to Add Environment Variables in Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to **Settings** → **Environment Variables**
4. Click **Add New**
5. Enter the **Key** (e.g., `SECRET_KEY`)
6. Enter the **Value** (e.g., your secret key)
7. Select the **Environments** (Production, Preview, Development)
8. Click **Save**
9. **Redeploy** your application for changes to take effect

## Minimum Required Variables for Basic Functionality

At minimum, you MUST set these three variables:
- `SECRET_KEY`
- `DEBUG=False`
- `DATABASE_URL`

Without these, your application will fail with a 500 error.

## Troubleshooting

### Error: "SECRET_KEY environment variable must be set in production"
- **Solution**: Add `SECRET_KEY` environment variable in Vercel Dashboard

### Error: "FUNCTION_INVOCATION_FAILED"
- **Common causes**:
  1. Missing `SECRET_KEY`
  2. Missing `DATABASE_URL` (if database is required)
  3. Database connection issues
  4. Missing migrations (run migrations manually)
  5. Import errors in code

### Database Connection Errors
- **Solution**: 
  1. Verify `DATABASE_URL` is correct
  2. Ensure database allows connections from Vercel IPs
  3. Check database credentials are correct
  4. Run migrations: `python manage.py migrate` (via Vercel CLI or after deployment)

### Static Files Not Loading
- **Solution**:
  1. If using AWS S3: Set `USE_AWS=True` and AWS credentials
  2. If not using AWS: Ensure WhiteNoise middleware is working (already configured)
  3. Collect static files: `python manage.py collectstatic --noinput`
