/*
 * CoreZ starter YARA ruleset.
 * Conservative, general-purpose rules for pattern-based detection beyond the
 * MD5 hash blacklist. Extend this file (or drop more .yar files in this folder)
 * to grow coverage.
 */

rule EICAR_Test_File
{
    meta:
        description = "EICAR standard antivirus test string (harmless)"
        severity    = "test"
        reference   = "https://www.eicar.org/download-anti-malware-testfile/"
    strings:
        $eicar = "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
    condition:
        $eicar
}

rule Suspicious_Windows_Shell_Exec
{
    meta:
        description = "Script invoking shell/download primitives often used by droppers"
        severity    = "suspicious"
    strings:
        $s1 = "powershell" nocase
        $s2 = "-EncodedCommand" nocase
        $s3 = "DownloadString" nocase
        $s4 = "WScript.Shell" nocase
        $s5 = "cmd.exe /c" nocase
    condition:
        2 of ($s*)
}

rule Suspicious_Base64_PE_Blob
{
    meta:
        description = "Base64-encoded PE header embedded in a text/script file"
        severity    = "suspicious"
    strings:
        // "TVqQAA" / "TVpQAA" are base64 of the MZ...PE header prefix.
        $b64_mz1 = "TVqQAA"
        $b64_mz2 = "TVpQAA"
    condition:
        any of them
}

rule Linux_Reverse_Shell_OneLiner
{
    meta:
        description = "Common Linux reverse-shell one-liners"
        severity    = "suspicious"
    strings:
        $bash = "/dev/tcp/"
        $nc1  = "nc -e /bin/sh" nocase
        $nc2  = "ncat -e /bin/bash" nocase
        $py   = "socket.socket(socket.AF_INET"
    condition:
        any of them
}
