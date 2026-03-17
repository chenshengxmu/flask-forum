# BBS Forum - Quick Reference Guide

## Server Commands

### Start Server
```bash
source venv/bin/activate
python run.py
```

### Start in Background
```bash
source venv/bin/activate
nohup python run.py > server.log 2>&1 &
```

### Stop Server
```bash
# Find process ID
ps aux | grep "python run.py"

# Kill process
kill <PID>
```

### Check Server Status
```bash
curl http://localhost:5001/
```

---

## Testing Commands

### Run All Tests
```bash
# Functional tests
python test_refactoring_simple.py

# Query optimization tests
python test_query_optimization.py

# Service layer tests
python test_services.py
```

### Quick Health Check
```bash
# Test homepage
curl -s -o /dev/null -w "Status: %{http_code}, Time: %{time_total}s\n" http://localhost:5001/

# Test category page
curl -s -o /dev/null -w "Status: %{http_code}\n" http://localhost:5001/category/1

# Test post page
curl -s -o /dev/null -w "Status: %{http_code}\n" http://localhost:5001/post/1
```

---

## Database Commands

### Run Migrations
```bash
flask db upgrade
```

### Create New Migration
```bash
flask db migrate -m "Description of changes"
```

### Rollback Migration
```bash
flask db downgrade
```

### Check Current Migration
```bash
flask db current
```

---

## Log Commands

### View Logs
```bash
# Application log
tail -f logs/app.log

# Error log
tail -f logs/error.log

# Access log
tail -f logs/access.log

# All logs
tail -f logs/*.log
```

### Search Logs
```bash
# Find errors
grep ERROR logs/app.log

# Find specific user activity
grep "username" logs/access.log

# Find slow requests (> 100ms)
grep -E "[0-9]{3,}ms" logs/access.log
```

---

## Git Commands

### Check Status
```bash
git status
```

### View Recent Commits
```bash
git log --oneline -5
```

### Push Changes
```bash
git push origin main
```

### View Changes
```bash
git diff
```

---

## Access URLs

### Frontend
- Homepage: http://localhost:5001/
- Category: http://localhost:5001/category/1
- Post: http://localhost:5001/post/1
- Login: http://localhost:5001/auth/login
- Register: http://localhost:5001/auth/register

### Admin
- Admin Panel: http://localhost:5001/admin

---

## Performance Monitoring

### Check Query Count
```python
# Enable SQL query logging in config.py
LOG_SQL_QUERIES = True

# View database.log
tail -f logs/database.log
```

### Benchmark Pages
```bash
# Homepage
time curl -s http://localhost:5001/ > /dev/null

# Category page
time curl -s http://localhost:5001/category/1 > /dev/null

# Post page
time curl -s http://localhost:5001/post/1 > /dev/null
```

---

## Troubleshooting

### Server Won't Start
```bash
# Check if port is already in use
lsof -i :5001

# Kill process on port
kill $(lsof -t -i:5001)
```

### Database Locked
```bash
# Check for database locks
fuser bbs_forum.db

# Force close connections
rm bbs_forum.db-journal
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

### Permission Denied
```bash
# Fix permissions
chmod +x run.py
chmod -R 755 app/
```

---

## Development Workflow

### 1. Start Development
```bash
# Activate virtual environment
source venv/bin/activate

# Start server
python run.py
```

### 2. Make Changes
```bash
# Edit code
# Test changes manually
# Run tests
```

### 3. Commit Changes
```bash
# Stage changes
git add <files>

# Commit
git commit -m "Description"

# Push
git push origin main
```

### 4. Deploy
```bash
# Stop server
kill <PID>

# Pull changes
git pull origin main

# Run migrations
flask db upgrade

# Start server
python run.py
```

---

## Key Files

### Configuration
- `config.py` - Application configuration
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (create from .env.example)

### Application
- `run.py` - Application entry point
- `app/__init__.py` - App factory
- `app/models.py` - Database models
- `app/routes/` - Route handlers
- `app/services/` - Business logic
- `app/utils/` - Utility functions

### Database
- `bbs_forum.db` - SQLite database
- `migrations/` - Database migrations

### Tests
- `test_refactoring_simple.py` - Functional tests
- `test_query_optimization.py` - Performance tests
- `test_services.py` - Service layer tests

### Documentation
- `README.md` - Project overview
- `REFACTORING_PROGRESS.md` - Refactoring progress
- `PHASE_1_2_COMPLETE.md` - Phase 1 & 2 documentation
- `TEST_RESULTS.md` - Test results
- `VERIFICATION_REPORT.md` - Verification report
- `QUICK_REFERENCE.md` - This file

---

## Common Tasks

### Add New Feature
1. Create service method in `app/services/`
2. Add route in `app/routes/`
3. Create/update template in `app/templates/`
4. Add tests
5. Update documentation

### Fix Bug
1. Reproduce bug
2. Check logs for errors
3. Fix code
4. Add test to prevent regression
5. Commit fix

### Optimize Performance
1. Enable SQL query logging
2. Identify slow queries
3. Add indexes or optimize queries
4. Test with `test_query_optimization.py`
5. Verify improvements

### Deploy to Production
1. Update configuration for production
2. Use PostgreSQL instead of SQLite
3. Set DEBUG = False
4. Configure proper SECRET_KEY
5. Setup reverse proxy (nginx)
6. Enable HTTPS
7. Setup monitoring

---

## Performance Targets

### Current Performance (After Refactoring)
- Homepage: 3ms (2 queries)
- Category: 8ms (2 queries)
- Post: 4ms (3 queries)
- Average: 5ms

### Targets Met
- ✅ < 500ms load time
- ✅ < 5 queries per page
- ✅ 90%+ query reduction
- ✅ N+1 problem eliminated

---

## Security Checklist

### Implemented
- [x] XSS protection (HTML sanitization)
- [x] File upload validation (magic bytes)
- [x] Secure filenames (random generation)
- [x] Authorization decorators
- [x] Error handling with rollback
- [x] Comprehensive logging

### TODO (Phase 5)
- [ ] Rate limiting
- [ ] CSRF protection (WTForms has it)
- [ ] Security headers
- [ ] HTTPS enforcement
- [ ] Session security

---

## Support

### Get Help
- View documentation: `docs/`
- Check logs: `logs/`
- Run tests: `python test_*.py`
- GitHub issues: https://github.com/chenshengxmu/flask-forum/issues

### Report Issues
1. Check logs for errors
2. Try to reproduce
3. Document steps to reproduce
4. Create GitHub issue with details

---

**Last Updated:** 2026-03-17
**Version:** Phase 1 & 2 Complete
**Status:** Production Ready (after Phase 5 config)
