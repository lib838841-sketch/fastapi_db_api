import argparse
import subprocess
import os
import sys

def run_command(command, env=None):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, env=env)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Exception: {e}")
        return False

def backup_table(host, port, user, password, dbname, table_name, backup_file):
    """Backup a single table."""
    env = os.environ.copy()
    env['PGPASSWORD'] = password
    command = f"pg_dump -h {host} -p {port} -U {user} -t {table_name} -F c -f {backup_file} {dbname}"
    print(f"Running backup command: {command}")
    return run_command(command, env)

def backup_database(host, port, user, password, dbname, backup_file):
    """Backup an entire database."""
    env = os.environ.copy()
    env['PGPASSWORD'] = password
    command = f"pg_dump -h {host} -p {port} -U {user} -F c -f {backup_file} {dbname}"
    print(f"Running backup command: {command}")
    return run_command(command, env)

def backup_instance(host, port, user, password, backup_file):
    """Backup the entire instance (all databases)."""
    env = os.environ.copy()
    env['PGPASSWORD'] = password
    command = f"pg_dumpall -h {host} -p {port} -U {user} -f {backup_file}"
    print(f"Running backup command: {command}")
    return run_command(command, env)

def restore_table(host, port, user, password, dbname, table_name, backup_file):
    """Restore a single table."""
    env = os.environ.copy()
    env['PGPASSWORD'] = password
    command = f"pg_restore -h {host} -p {port} -U {user} -t {table_name} -d {dbname} {backup_file}"
    print(f"Running restore command: {command}")
    return run_command(command, env)

def restore_database(host, port, user, password, dbname, backup_file):
    """Restore an entire database."""
    env = os.environ.copy()
    env['PGPASSWORD'] = password
    command = f"pg_restore -h {host} -p {port} -U {user} -d {dbname} {backup_file}"
    print(f"Running restore command: {command}")
    return run_command(command, env)

def restore_instance(host, port, user, password, backup_file):
    """Restore the entire instance."""
    env = os.environ.copy()
    env['PGPASSWORD'] = password
    # For instance restore, use psql since pg_dumpall produces SQL
    command = f"psql -h {host} -p {port} -U {user} -f {backup_file}"
    print(f"Running restore command: {command}")
    return run_command(command, env)

def main():
    parser = argparse.ArgumentParser(description="Backup and Restore OpenGauss Database")
    parser.add_argument('action', choices=['backup', 'restore'], help='Action to perform')
    parser.add_argument('level', choices=['table', 'database', 'instance'], help='Backup/Restore level')
    parser.add_argument('--host', required=True, help='Database host')
    parser.add_argument('--port', required=True, help='Database port')
    parser.add_argument('--user', required=True, help='Database user')
    parser.add_argument('--password', required=True, help='Database password')
    parser.add_argument('--dbname', help='Database name (required for table and database levels)')
    parser.add_argument('--table', help='Table name (required for table level)')
    parser.add_argument('--file', required=True, help='Backup file path')

    args = parser.parse_args()

    if args.level in ['table', 'database'] and not args.dbname:
        print("Error: --dbname is required for table and database levels")
        sys.exit(1)

    if args.level == 'table' and not args.table:
        print("Error: --table is required for table level")
        sys.exit(1)

    success = False

    if args.action == 'backup':
        if args.level == 'table':
            success = backup_table(args.host, args.port, args.user, args.password, args.dbname, args.table, args.file)
        elif args.level == 'database':
            success = backup_database(args.host, args.port, args.user, args.password, args.dbname, args.file)
        elif args.level == 'instance':
            success = backup_instance(args.host, args.port, args.user, args.password, args.file)
    elif args.action == 'restore':
        if args.level == 'table':
            success = restore_table(args.host, args.port, args.user, args.password, args.dbname, args.table, args.file)
        elif args.level == 'database':
            success = restore_database(args.host, args.port, args.user, args.password, args.dbname, args.file)
        elif args.level == 'instance':
            success = restore_instance(args.host, args.port, args.user, args.password, args.file)

    if success:
        print(f"{args.action.capitalize()} {args.level} completed successfully.")
    else:
        print(f"{args.action.capitalize()} {args.level} failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
