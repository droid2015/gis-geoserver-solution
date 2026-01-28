#!/usr/bin/env python3
"""
Script hoàn chỉnh để update tất cả documentation sang stack 2026
Repository: droid2015/gis-geoserver-solution
Updated: 2026-01-28

Usage:
    python update_all_docs_2026.py
"""

import os
import re
from pathlib import Path
from datetime import datetime
import shutil

# ============================================================================
# COLORS
# ============================================================================

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;36m'
    CYAN = '\033[0;96m'
    MAGENTA = '\033[0;95m'
    NC = '\033[0m'

def print_header(text):
    print(f"\n{Colors.CYAN}{'='*80}{Colors.NC}")
    print(f"{Colors.CYAN}{text.center(80)}{Colors.NC}")
    print(f"{Colors.CYAN}{'='*80}{Colors.NC}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.NC}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.NC}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.NC}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.NC}")

# ============================================================================
# VERSION MAPPINGS
# ============================================================================

VERSION_UPDATES = {
    # OS - Ubuntu
    (r'Ubuntu 22\.04', 'Ubuntu 24.04'),
    (r'Ubuntu Server 22\.04', 'Ubuntu Server 24.04'),
    (r'Ubuntu 20\.04', 'Ubuntu 24.04'),
    (r'ubuntu:22\.04', 'ubuntu:24.04'),
    (r'Focal Fossa', 'Noble Numbat'),
    (r'Jammy Jellyfish', 'Noble Numbat'),
    
    # Kernel
    (r'Kernel:?\s*5\.15', 'Kernel: 6.8'),
    (r'kernel 5\.15', 'kernel 6.8'),
    (r'5\.15\.0-\d+-generic', '6.8.0-xx-generic'),
    
    # Python
    (r'Python:?\s*3\.10', 'Python: 3.12'),
    (r'Python 3\.10', 'Python 3.12'),
    (r'python3\.10', 'python3.12'),
    (r'python:3\.10', 'python:3.12'),
    (r'Python:?\s*3\.11', 'Python: 3.12'),
    
    # PostgreSQL
    (r'PostgreSQL:?\s*14', 'PostgreSQL: 16'),
    (r'PostgreSQL 14', 'PostgreSQL 16'),
    (r'postgresql-14', 'postgresql-16'),
    (r'postgres:14', 'postgres:16'),
    (r'PostgreSQL:?\s*15', 'PostgreSQL: 16'),
    (r'psql \(PostgreSQL\) 14', 'psql (PostgreSQL) 16'),
    
    # PostGIS
    (r'PostGIS:?\s*3\.2', 'PostGIS: 3.4'),
    (r'PostGIS 3\.2', 'PostGIS 3.4'),
    (r'postgis-3\.2', 'postgis-3.4'),
    (r'postgis:3\.2', 'postgis:3.4'),
    (r'postgresql-14-postgis-3', 'postgresql-16-postgis-3'),
    (r'PostGIS:?\s*3\.3', 'PostGIS: 3.4'),
    (r'PostGIS 3\.3', 'PostGIS 3.4'),
    
    # GeoServer - MOST IMPORTANT
    (r'GeoServer:?\s*2\.25\.0', 'GeoServer: 2.28.2'),
    (r'GeoServer 2\.25\.0', 'GeoServer 2.28.2'),
    (r'GeoServer:?\s*2\.25', 'GeoServer: 2.28.2'),
    (r'GeoServer 2\.25', 'GeoServer 2.28.2'),
    (r'geoserver:2\.25\.0', 'geoserver:2.28.2'),
    (r'geoserver-2\.25\.0', 'geoserver-2.28.2'),
    (r'geoserver/2\.25', 'geoserver/2.28.2'),
    (r'GeoServer:?\s*2\.20', 'GeoServer: 2.28.2'),
    (r'GeoServer:?\s*2\.24', 'GeoServer: 2.28.2'),
    (r'kartoza/geoserver:2\.25\.0', 'docker.osgeo.org/geoserver:2.28.2'),
    
    # GeoWebCache
    (r'GeoWebCache:?\s*1\.25', 'GeoWebCache: 1.28'),
    (r'GeoWebCache 1\.25', 'GeoWebCache 1.28'),
    (r'GeoWebCache:?\s*1\.24', 'GeoWebCache: 1.28'),
    
    # QGIS
    (r'QGIS:?\s*3\.22', 'QGIS: 3.34'),
    (r'QGIS 3\.22', 'QGIS 3.34'),
    (r'QGIS:?\s*3\.28', 'QGIS: 3.34'),
    (r'QGIS:?\s*3\.30', 'QGIS: 3.34'),
    (r'QGIS 3\.28', 'QGIS 3.34'),
    (r'Prizren', 'Prizren'),  # Keep same (3.34 LTR)
    
    # Java
    (r'Java:?\s*11', 'Java: 17'),
    (r'OpenJDK 11', 'OpenJDK 17'),
    (r'openjdk-11', 'openjdk-17'),
    (r'java-11', 'java-17'),
    (r'jdk-11', 'jdk-17'),
    
    # Node.js
    (r'Node\.js:?\s*16', 'Node.js: 20'),
    (r'Node\.js 16', 'Node.js 20'),
    (r'node:16', 'node:20'),
    (r'nodejs 16', 'nodejs 20'),
    (r'Node\.js:?\s*18', 'Node.js: 20'),
    (r'setup_16\.x', 'setup_20.x'),
    
    # React
    (r'React:?\s*17', 'React: 18'),
    (r'React 17', 'React 18'),
    (r'"react": "\^17', '"react": "^18'),
    
    # OpenLayers
    (r'OpenLayers:?\s*8', 'OpenLayers: 9'),
    (r'OpenLayers 8', 'OpenLayers 9'),
    (r'OpenLayers:?\s*7', 'OpenLayers: 9'),
    (r'"ol": "\^8', '"ol": "^9'),
    
    # Docker
    (r'Docker:?\s*20\.\d+', 'Docker: 26.x'),
    (r'Docker 20\.\d+', 'Docker 26.x'),
    (r'Docker:?\s*24\.\d+', 'Docker: 26.x'),
    (r'Docker:?\s*25\.\d+', 'Docker: 26.x'),
    
    # Nginx
    (r'Nginx:?\s*1\.18', 'Nginx: 1.25'),
    (r'Nginx:?\s*1\.20', 'Nginx: 1.25'),
    (r'Nginx:?\s*1\.22', 'Nginx: 1.25'),
    (r'nginx:1\.2[0-4]', 'nginx:1.25'),
    
    # Redis
    (r'Redis:?\s*6', 'Redis: 7'),
    (r'redis:6', 'redis:7'),
    
    # GDAL
    (r'GDAL:?\s*3\.6', 'GDAL: 3.8'),
    (r'GDAL:?\s*3\.7', 'GDAL: 3.8'),
    (r'GDAL 3\.6', 'GDAL 3.8'),
    
    # Git
    (r'Git:?\s*2\.3[0-9]', 'Git: 2.43'),
    (r'Git 2\.3[0-9]', 'Git 2.43'),
    
    # FastAPI
    (r'FastAPI:?\s*0\.10[0-5]', 'FastAPI: 0.109'),
    (r'fastapi==0\.10[0-5]', 'fastapi==0.109'),
    
    # SQLAlchemy
    (r'SQLAlchemy:?\s*1\.\d+', 'SQLAlchemy: 2.0'),
    (r'sqlalchemy==1\.\d+', 'sqlalchemy==2.0'),
}

DATE_UPDATES = [
    (r'Updated:\s*\d{4}-\d{2}-\d{2}', f'Updated: {datetime.now().strftime("%Y-%m-%d")}'),
    (r'Last Updated:\s*\d{4}-\d{2}-\d{2}', f'Last Updated: {datetime.now().strftime("%Y-%m-%d")}'),
    (r'Date:\s*\d{4}-\d{2}-\d{2}', f'Date: {datetime.now().strftime("%Y-%m-%d")}'),
    (r'## Updated: \d{4}-\d{2}-\d{2}', f'## Updated: {datetime.now().strftime("%Y-%m-%d")}'),
]

# ============================================================================
# FUNCTIONS
# ============================================================================

def find_all_md_files(root_dir='.'):
    """Find all .md files"""
    md_files = []
    exclude_dirs = {'node_modules', 'venv', '.venv', 'env', '.git', 'build', 'dist'}
    
    for path in Path(root_dir).rglob('*.md'):
        # Check if any parent directory is in exclude list
        if any(exclude in path.parts for exclude in exclude_dirs):
            continue
        md_files.append(path)
    
    return sorted(md_files)

def backup_file(filepath):
    """Create backup of file"""
    backup_path = f"{filepath}.backup"
    shutil.copy2(filepath, backup_path)
    return backup_path

def update_file_content(filepath):
    """Update content of a file"""
    try:
        # Read file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        updates_made = []
        
        # Apply version updates
        for pattern, replacement in VERSION_UPDATES:
            matches = list(re.finditer(pattern, content, re.IGNORECASE))
            if matches:
                count = len(matches)
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
                updates_made.append(f"{pattern[:30]}... → {replacement[:30]}... ({count}x)")
        
        # Apply date updates
        for pattern, replacement in DATE_UPDATES:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                if "Date updated" not in str(updates_made):
                    updates_made.append("Dates updated")
        
        # Check if changes were made
        if content != original_content:
            # Backup original
            backup_path = backup_file(filepath)
            
            # Write updated content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True, updates_made, backup_path
        else:
            return False, [], None
            
    except Exception as e:
        print_error(f"Error processing {filepath}: {e}")
        return False, [], None

def create_summary_report(results):
    """Create summary report"""
    report = []
    report.append("\n" + "="*80)
    report.append(" DETAILED UPDATE REPORT")
    report.append("="*80 + "\n")
    
    # Group by status
    updated = [r for r in results if r['updated']]
    skipped = [r for r in results if not r['updated']]
    
    report.append(f"📊 Summary:")
    report.append(f"   Total files:    {len(results)}")
    report.append(f"   Updated:        {len(updated)} ✅")
    report.append(f"   Skipped:        {len(skipped)} ⏭️")
    report.append("")
    
    if updated:
        report.append("📝 Updated Files:")
        report.append("")
        for r in updated:
            report.append(f"   ✅ {r['file']}")
            for update in r['updates'][:2]:  # Show first 2 updates
                report.append(f"      • {update}")
            if len(r['updates']) > 2:
                report.append(f"      ... and {len(r['updates']) - 2} more")
            report.append("")
    
    report.append("="*80)
    
    return "\n".join(report)

def save_report(report_text):
    """Save report to file"""
    report_file = f"update_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_text)
    return report_file

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main function"""
    print_header("UPDATE ALL DOCUMENTATION TO 2026 STACK")
    print(f"{Colors.BLUE}Repository: droid2015/gis-geoserver-solution{Colors.NC}")
    print(f"{Colors.BLUE}Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.NC}\n")
    
    # Find files
    print_info("Searching for markdown files...")
    md_files = find_all_md_files()
    print_success(f"Found {len(md_files)} markdown files\n")
    
    # Show what will be updated
    print_info("Version updates that will be applied:")
    updates = [
        ("Ubuntu", "22.04 → 24.04 LTS"),
        ("Python", "3.10 → 3.12"),
        ("PostgreSQL", "14 → 16"),
        ("PostGIS", "3.2 → 3.4"),
        ("GeoServer", "2.25.0 → 2.28.2 ⭐"),
        ("GeoWebCache", "1.25 → 1.28"),
        ("Java", "11 → 17"),
        ("Node.js", "16 → 20"),
        ("Docker", "20.x → 26.x"),
        ("OpenLayers", "8 → 9"),
        ("QGIS", "3.22 → 3.34"),
        ("Nginx", "1.22 → 1.25"),
        ("Redis", "6 → 7"),
    ]
    
    for name, change in updates:
        print(f"   • {name:15} {change}")
    print()
    
    # Confirm
    print_warning("This will modify all markdown files!")
    print("Backups will be created with .backup extension\n")
    
    response = input(f"{Colors.YELLOW}Proceed? (yes/no): {Colors.NC}")
    if response.lower() != 'yes':
        print_error("Aborted by user")
        return
    
    print()
    print_header("PROCESSING FILES")
    
    # Process files
    results = []
    updated_count = 0
    skipped_count = 0
    error_count = 0
    
    for i, filepath in enumerate(md_files, 1):
        relative_path = filepath.relative_to('.')
        
        print(f"\n[{i}/{len(md_files)}] Processing: {Colors.CYAN}{relative_path}{Colors.NC}")
        
        updated, updates, backup_path = update_file_content(filepath)
        
        result = {
            'file': str(relative_path),
            'updated': updated,
            'updates': updates,
            'backup': backup_path
        }
        results.append(result)
        
        if updated:
            print_success(f"Updated ({len(updates)} changes)")
            for update in updates[:2]:
                print(f"   • {update}")
            if len(updates) > 2:
                print(f"   ... and {len(updates) - 2} more")
            print(f"   Backup: {Colors.BLUE}{backup_path}{Colors.NC}")
            updated_count += 1
        else:
            print(f"{Colors.BLUE}⏭️  No changes needed{Colors.NC}")
            skipped_count += 1
    
    # Create and display report
    report_text = create_summary_report(results)
    print(report_text)
    
    # Save report
    report_file = save_report(report_text)
    print_success(f"Report saved to: {report_file}\n")
    
    # Next steps
    print_header("NEXT STEPS")
    print(f"{Colors.GREEN}1. Review changes:{Colors.NC}")
    print(f"   git diff")
    print()
    print(f"{Colors.GREEN}2. Check specific files:{Colors.NC}")
    print(f"   cat {md_files[0]}")
    print()
    print(f"{Colors.GREEN}3. Test documentation:{Colors.NC}")
    print(f"   • Open files in VS Code/browser")
    print(f"   • Verify markdown renders correctly")
    print()
    print(f"{Colors.GREEN}4. If satisfied, commit:{Colors.NC}")
    print(f"   git add docs/")
    print(f"   git commit -m 'docs: update all versions to 2026 stack'")
    print()
    print(f"{Colors.GREEN}5. If issues, restore backups:{Colors.NC}")
    print(f"   find . -name '*.backup' -exec bash -c 'mv \"$0\" \"${{0%.backup}}\"' {{}} \\;")
    print()
    print(f"{Colors.GREEN}6. Clean up backups after commit:{Colors.NC}")
    print(f"   find . -name '*.backup' -delete")
    print()
    
    print_success("Update complete! 🎉\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Interrupted by user{Colors.NC}")
    except Exception as e:
        print(f"\n\n{Colors.RED}❌ ERROR: {e}{Colors.NC}")
        import traceback
        traceback.print_exc()