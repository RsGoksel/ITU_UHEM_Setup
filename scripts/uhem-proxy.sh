#!/bin/bash
# Only starts the explicitly configured UHEM service. Never deletes interfaces/routes.
set -euo pipefail
if [[ $# != 2 || $1 != altay.uhem.itu.edu.tr || $2 != 22 ]]; then
    printf '%s\n' 'This proxy only supports altay.uhem.itu.edu.tr port22.' >&2
    exit 2
fi
service=${UHEM_VPN_SERVICE:-uhem-vpn.service}
tunnel=${UHEM_TUN_DEVICE:-tun-uhem}
dns=${UHEM_VPN_DNS:-10.128.5.2}
if [[ ! $service =~ ^[A-Za-z0-9][A-Za-z0-9_.@-]*\.service$ || ! $tunnel =~ ^[A-Za-z0-9][A-Za-z0-9_.-]{0,14}$ || ! $dns =~ ^10\.128\.([0-9]{1,3})\.([0-9]{1,3})$ ]]; then
    printf '%s\n' 'Invalid service, tunnel or internal DNS setting.' >&2
    exit 2
fi
[[ $dns =~ ^10\.128\.([0-9]{1,3})\.([0-9]{1,3})$ ]]
if (( 10#${BASH_REMATCH[1]} > 255 || 10#${BASH_REMATCH[2]} > 255 )); then
    printf '%s\n' 'Invalid internal DNS address.' >&2
    exit 2
fi
for dependency in systemctl dig ip nc; do
    command -v "$dependency" >/dev/null || { printf '%s\n' "Missing command: $dependency" >&2; exit 1; }
done
if ! systemctl is-active --quiet "$service"; then
    systemctl start "$service" || { printf '%s\n' 'Start the configured UHEM VPN service with authorized privileges first.' >&2; exit 1; }
fi
for ((attempt=0; attempt<20; attempt++)); do
    answer=$(dig +short +time=1 +tries=1 @"$dns" "$1" A 2>/dev/null || true)
    target=''
    while IFS= read -r address; do
        if [[ $address =~ ^10\.128\.([0-9]{1,3})\.([0-9]{1,3})$ ]]; then
            (( 10#${BASH_REMATCH[1]} <= 255 && 10#${BASH_REMATCH[2]} <= 255 )) || continue
            route=$(ip -4 route get "$address" 2>/dev/null || true)
            if [[ " $route " == *" dev $tunnel "* ]]; then
                target=$address
                break
            fi
        fi
    done <<< "$answer"
    if [[ -n $target ]]; then
        # Run outside the read loop: nc must inherit SSH stdin, not the DNS here-string.
        # SSH ConnectTimeout bounds connection setup; no nc idle timeout.
        exec nc "$target" "$2"
    fi
    systemctl is-active --quiet "$service" || { printf '%s\n' 'UHEM VPN service stopped; inspect its private log.' >&2; exit 1; }
    sleep 0.5
done
printf '%s\n' 'Internal DNS/route not ready on the configured UHEM tunnel. No public-DNS fallback was attempted.' >&2
exit 1
