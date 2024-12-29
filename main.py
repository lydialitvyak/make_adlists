#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os


def fetch_hosts(url):
    """
    指定したURLからhostsファイル(テキスト)を取得し、行ごとのリストを返す。
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.splitlines()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return []


def clean_hosts(lines):
    """
    コメント行や空行を取り除き、重複を除去して返す。
    """
    cleaned = set()
    for line in lines:
        # 前後の空白除去
        line = line.strip()
        if not line:
            continue  # 空行はスキップ

        # hostsファイルのコメント例: #, ! などで始まる行
        # ここで他にも特殊な書式(! で始まるAdblock記法など)を考慮する場合は追加
        if line.startswith("#") or line.startswith("!"):
            continue

        # 重複除外のためにsetを利用
        cleaned.add(line)

    return list(cleaned)


def combine_lists(url_list):
    """
    URLのリストをまとめてダウンロードし、クリーンアップしたリストをまとめる。
    """
    combined = []
    for url in url_list:
        print(f"Fetching from {url} ...")
        lines = fetch_hosts(url)
        cleaned = clean_hosts(lines)
        combined.extend(cleaned)
    # 最後にまとめたhostsをさらに重複除外 (万一URL間に被りがある場合)
    combined = list(set(combined))
    return combined


def write_hosts_to_file(combined_hosts, output_file):
    """
    結果をテキストファイルとして書き出す。
    """
    print(f"Writing {len(combined_hosts)} lines to {output_file} ...")
    with open(output_file, "w", encoding="utf-8") as f:
        for line in sorted(combined_hosts):
            f.write(line + "\n")
    print("Done.")


##########################################
# テスト用関数
##########################################


def test_fetch_hosts():
    """
    fetch_hosts()の簡易テスト。
    適当なURLから行数を取得できればOKとする。
    """
    test_url = (
        "https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt"
    )
    lines = fetch_hosts(test_url)
    if len(lines) > 0:
        print("[TEST] test_fetch_hosts: OK")
    else:
        print("[TEST] test_fetch_hosts: FAIL")


def test_clean_hosts():
    """
    clean_hosts()の簡易テスト。
    コメント行の除去、空行の除去、重複除去ができているか確認する。
    """
    test_lines = [
        "# This is comment line",
        "! Another comment line",
        "     ",
        "0.0.0.0 example.com",
        "0.0.0.0 example.com",
    ]
    cleaned = clean_hosts(test_lines)
    if len(cleaned) == 1 and "0.0.0.0 example.com" in cleaned:
        print("[TEST] test_clean_hosts: OK")
    else:
        print("[TEST] test_clean_hosts: FAIL")


##########################################
# メイン関数
##########################################


def main():
    """
    実行時に呼び出されるメイン処理。
    """
    # テスト実行 (必要な場合は実行してください)
    # test_fetch_hosts()
    # test_clean_hosts()

    # list.md から得たURLをまとめたリスト(すべて挙げると長いので一例)
    url_list = [
        # 1
        "https://raw.githubusercontent.com/DandelionSprout/adfilt/master/Alternate%20versions%20Anti-Malware%20List/AntiMalwareHosts.txt",
        # 2
        "https://raw.githubusercontent.com/Goooler/1024_hosts/master/hosts",
        # 3
        "https://tgc.cloud/downloads/hosts.txt",
        # 4
        "https://o0.pages.dev/mini/hosts.txt",  # 1Hosts (Mini)
        # 5
        "https://o0.pages.dev/Lite/hosts.txt",  # 1Hosts (Lite)
        # 6
        "https://o0.pages.dev/Pro/hosts.txt",  # 1Hosts (Pro)
        # 7
        "https://o0.pages.dev/Xtra/hosts.txt",  # 1Hosts (Xtra)
        # 8
        # 1Hosts (kidSaf)
        "https://badmojr.gitlab.io/addons_1hosts/kidSaf/hosts.txt",
        # 9
        "https://raw.githubusercontent.com/jmhenrique/adblock/master/etc/adblock_hosts",
        # 10
        "https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/hosts.txt",
        # 11
        "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.2o7Net/hosts",
        # 12
        "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Risk/hosts",
        # 13
        "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Spam/hosts",
        # 14
        "https://raw.githubusercontent.com/r-a-y/mobile-hosts/master/AdguardDNS.txt",
        # 15
        "https://raw.githubusercontent.com/r-a-y/mobile-hosts/master/AdguardMobileAds.txt",
        # 16
        "https://raw.githubusercontent.com/r-a-y/mobile-hosts/master/AdguardMobileSpyware.txt",
        # 17
        "https://raw.githubusercontent.com/r-a-y/mobile-hosts/master/AdguardApps.txt",
        # 18
        "https://getadhell.com/standard-package.txt",
        # 19
        "https://repo.andnixsh.com/adblocker/hosts",
        # 20
        "https://raw.githubusercontent.com/furkun/AndroidSecurityHosts/main/hosts",
        # 21
        "https://raw.githubusercontent.com/yhonay/antipopads/master/hosts",
        # 22
        "https://raw.githubusercontent.com/CyanideBrother/anti-pr0n/master/hosts",
        # 23
        "https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt",
        # 24
        "https://raw.githubusercontent.com/anudeepND/blacklist/master/CoinMiner.txt",
        # 25
        "https://raw.githubusercontent.com/anudeepND/blacklist/master/facebook.txt",
        # 26
        "https://asc.hk/adplus.txt",
        # 27
        "https://raw.githubusercontent.com/mitchellkrogza/Badd-Boyz-Hosts/master/hosts",
        # 28
        "https://www.hostsfile.org/Downloads/hosts.txt",
        # 29
        "https://paulgb.github.io/BarbBlock/blacklists/hosts-file.txt",
        # 30
        "https://raw.githubusercontent.com/bjornstar/hosts/master/hosts",
        # 31
        "https://mkb2091.github.io/blockconvert/output/hosts.txt",
        # 32
        "https://sysctl.org/cameleon/hosts",
        # 33
        "https://raw.githubusercontent.com/cb-software/CB-Malicious-Domains/master/block_lists/hosts",
        # 34
        "https://gitlab.com/ZeroDot1/CoinBlockerLists/raw/master/hosts",
        # 35
        "https://gitlab.com/ZeroDot1/CoinBlockerLists/raw/master/hosts_browser",
        # 36
        "https://gitlab.com/ZeroDot1/CoinBlockerLists/raw/master/hosts_optional",
        # 37
        "https://raw.githubusercontent.com/bongochong/CombinedPrivacyBlockLists/master/newhosts-final.hosts",
        # 38
        "https://raw.githubusercontent.com/Cybo1927/Hosts/master/Fake%20News",
        # 39
        "https://raw.githubusercontent.com/Cybo1927/Hosts/master/Hosts",
        # 40
        "https://raw.githubusercontent.com/DataMaster-2501/DataMaster-Android-AdBlock-Hosts/master/hosts",
        # 41
        "https://raw.githubusercontent.com/dnswarden/blocklist/master/blacklist-formats/hosts",
        # 42
        "https://raw.githubusercontent.com/MetaMask/eth-phishing-detect/master/src/hosts.txt",
        # 43
        "https://raw.githubusercontent.com/kowith337/PersonalFilterListCollection/master/hosts/hosts_facebook0.txt",
        # 44
        "https://hostfiles.frogeye.fr/firstparty-trackers-hosts.txt",
        # 45
        "https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Hosts/GoodbyeAds.txt",
        # 46
        "https://raw.githubusercontent.com/kowith337/PersonalFilterListCollection/master/hosts/hosts_google_adservice_id.txt",
        # 47
        "https://raw.githubusercontent.com/Hakame-kun/uBlock-Filters-Indonesia/master/Windows%20Host/hosts",
        # 48
        "https://nixnet.services/hosts.txt",
        # 49
        "https://raw.githubusercontent.com/michaeltrimm/hosts-blocking/master/_hosts.txt",
        # 50
        "https://v.firebog.net/hosts/static/HPHosts/HostsAdServers.txt",
        # 51
        "https://v.firebog.net/hosts/static/HPHosts/Hostsemd.txt",
        # 52
        "https://v.firebog.net/hosts/static/HPHosts/Hostsexp.txt",
        # 53
        "https://v.firebog.net/hosts/static/HPHosts/Hostsfsa.txt",
        # 54
        "https://v.firebog.net/hosts/static/HPHosts/Hostsgrm.txt",
        # 55
        "https://v.firebog.net/hosts/static/HPHosts/Hostsmmt.txt",
        # 56
        "https://v.firebog.net/hosts/static/HPHosts/Hostspha.txt",
        # 57
        "https://raw.githubusercontent.com/infinitytec/blocklists/master/ads-and-trackers.txt",
        # 58
        "https://raw.githubusercontent.com/infinitytec/blocklists/master/scams-and-phishing.txt",
        # 59
        "https://tgc.cloud/downloads/iOSAds.txt",
        # 60
        "https://gitlab.com/intr0/iVOID.GitLab.io/raw/master/iVOID.hosts",
        # 61
        "https://raw.githubusercontent.com/lewisje/jansal/master/adblock/hosts",
        # 62
        "https://www.github.developerdan.com/hosts/lists/ads-and-tracking-extended.txt",
        # 63
        "https://www.github.developerdan.com/hosts/lists/amp-hosts-extended.txt",
        # 64
        "https://www.github.developerdan.com/hosts/lists/tracking-aggressive-extended.txt",
        # 65
        "https://raw.githubusercontent.com/w13d/adblockListABP-PiHole/master/list.txt",
        # 66
        "https://adblock.mahakala.is/",
        # 67
        "https://raw.githubusercontent.com/biroloter/Mobile-Ad-Hosts/master/hosts",
        # 68
        "https://winhelp2002.mvps.org/hosts.txt",
        # 69
        "https://raw.githubusercontent.com/nickspaargaren/no-google/master/categories/doubleclick.txt",
        # 70
        "https://raw.githubusercontent.com/hoshsadiq/adblock-nocoin-list/master/hosts.txt",
        # 71
        "https://hosts.nfz.moe/full/hosts",
        # 72
        "https://raw.githubusercontent.com/notracking/hosts-blocklists/master/hostnames.txt",
        # 73
        "https://hosts.oisd.nl/basic/",
        # 74
        "https://hosts.oisd.nl/",
        # 75
        "https://hosts.oisd.nl/nsfw/",
        # 76
        "https://curben.gitlab.io/malware-filter/urlhaus-filter-hosts-online.txt",
        # 77
        "https://gitlab.com/Kurobeats/phishing_hosts/raw/master/hosts",
        # 78
        "https://curben.gitlab.io/malware-filter/phishing-filter-hosts.txt",
        # 79
        "https://raw.githubusercontent.com/furkun/Anti-IP-Grabber-Hosts/main/hosts",
        # 80
        "https://curben.gitlab.io/malware-filter/pup-filter-hosts.txt",
        # 81
        "https://raw.githubusercontent.com/Rhys-H/hosts-list/master/HostsList.txt",
        # 82
        "https://raw.githubusercontent.com/durablenapkin/scamblocklist/master/hosts.txt",
        # 83
        "https://sebsauvage.net/hosts/hosts",
        # 84
        "https://raw.githubusercontent.com/smed79/blacklist/master/hosts.txt",
        # 85
        "https://raw.githubusercontent.com/nathanaccidentally/SystemHostsBlocker/master/hosts",
        # 86
        "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling/hosts",
        # 87
        "https://raw.githubusercontent.com/Th3M3/blocklists/master/malware.list",
        # 88
        "https://hostsfile.mine.nu/hosts0.txt",
        # 89
        "https://raw.githubusercontent.com/iam-py-test/my_filters_001/main/Alternative%20list%20formats/antimalware_hosts.txt",
        # 90
        "https://hosts.ubuntu101.co.za/hosts",
        # 91
        "https://warui.intaa.net/adhosts/hosts.txt",
        # 92
        "https://raw.githubusercontent.com/mtxadmin/ublock/master/hosts.txt",
        # 93
        "https://raw.githubusercontent.com/yous/YousList/master/hosts.txt",
        # 94
        "https://raw.githubusercontent.com/anudeepND/youtubeadsblacklist/master/hosts.txt",
    ]

    output_file = "combined_hosts.txt"

    combined_hosts = combine_lists(url_list)
    write_hosts_to_file(combined_hosts, output_file)


if __name__ == "__main__":
    main()
