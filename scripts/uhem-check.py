#!/usr/bin/env python3
"""Read-only checks through an existing SSH alias. No jobs or VPN edits."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

REMOTE = r'''
import datetime,getpass,json,socket,subprocess
checks={
 "project":["/ari/progs/uhem-bin/projelerim","-l"],
 "partitions":["scontrol","-o","show","partition"],
 "nodes":["sinfo","-N","-h","-o","%N|%P|%t|%c|%m|%G"],
 "my_jobs":["squeue","-h","-u",getpass.getuser(),"-o","%i|%P|%T|%M|%l"],
 "modules":["bash","-lc","module -t avail"]
}
result={"captured_at":datetime.datetime.now().astimezone().isoformat(),"hostname":socket.gethostname(),"user":getpass.getuser(),"checks":{}}
for name,args in checks.items():
 try:
  p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True,timeout=15)
  result["checks"][name]={"returncode":p.returncode,"stdout":p.stdout,"stderr":p.stderr}
 except (OSError,subprocess.TimeoutExpired) as e:
  result["checks"][name]={"error":type(e).__name__}
print(json.dumps(result))
'''


def ssh_command(host):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", host):
        raise ValueError("Geçerli bir SSH kısayolu belirtin; örnek: UHEM_Nanoparticle")
    return ["ssh", "-o", "BatchMode=yes", "-o", "NumberOfPasswordPrompts=0",
            "-o", "StrictHostKeyChecking=yes", "-o", "ConnectTimeout=20",
            host, "python3", "-"]


def summarize(data):
    if not isinstance(data, dict) or not isinstance(data.get("checks"), dict):
        raise ValueError("Uzak kontrol çıktısı beklenen JSON yapısında değil")
    checks = data.get("checks", {})
    required = ("project", "partitions", "nodes", "my_jobs", "modules")
    failures = [name for name in required
                if not isinstance(checks.get(name), dict) or checks[name].get("returncode") != 0]
    project_check = checks.get("project")
    project = project_check.get("stdout", "") if isinstance(project_check, dict) else ""
    if not isinstance(project, str):
        project = ""
    summaries = []
    for line in project.splitlines():
        match = re.search(r"^\s*(\S+) .*CpuHour-Usage\):\s*([\d,]+)/([\d,]+).*Disk:\s*([\d,]+)/([\d,]+)", line)
        if match:
            account, used, total, disk_used, disk_total = match.groups()
            used, total, disk_used, disk_total = [int(s.replace(",", "")) for s in [used, total, disk_used, disk_total]]
            summaries.append({"account": account, "used_core_hours": used,
                              "total_core_hours": total, "remaining_core_hours": total-used,
                              "disk_used_gb": disk_used, "disk_total_gb": disk_total})
    if not summaries:
        failures.append("quota_not_parsed")
    return {"status": "PASS" if not failures else "PARTIAL",
            "hostname": data.get("hostname"), "user": data.get("user"),
            "projects": summaries, "failed_checks": failures,
            "jobs_submitted": 0, "read_only": True}


def save_report(path, data):
    path = Path(path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="UHEM_Nanoparticle", help="Mevcut SSH kısayolu")
    parser.add_argument("--output", help="Ham yerel rapor; yeni dosya, mod0600; Git'e eklemeyin")
    parser.add_argument("--local-only", action="store_true", help="SSH bağlantısı kurmadan yerel araçları denetle")
    args = parser.parse_args()
    try:
        command = ssh_command(args.host)
        if not shutil.which("ssh"):
            raise ValueError("OpenSSH istemcisi bulunamadı")
        if args.local_only:
            print(json.dumps({"status": "PASS_LOCAL_ONLY", "ssh_available": True,
                              "remote_verified": False, "jobs_submitted": 0}))
            return 0
        process = subprocess.run(command, input=REMOTE, text=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=110)
        if process.returncode:
            raise ValueError("SSH kontrolü başarısız. Normal ssh ile kimlik/host anahtarını doğrulayın; araç parola istemez ve anahtarı kendiliğinden kabul etmez.")
        data = json.loads(process.stdout)
        summary = summarize(data)
        if args.output:
            save_report(args.output, {"summary": summary, "remote": data})
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0 if summary["status"] == "PASS" else 1
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        print("Kontrol tamamlanamadı: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
