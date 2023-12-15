Get-Content "rockyou.txt" | ForEach-Object {
#Get-Content "20200419-Danish-words.txt" | ForEach-Object {
#Get-Content "dk_breach.txt" | ForEach-Object {
	$i = $_
	Write-Host "PASS: $i"
	& "C:\Program Files (x86)\UHARC CMD\bin\uharc.exe" e -pw$i "nissearkivet.uha" *>$null #2>&1
	$exitCode = $LASTEXITCODE

	if ($exitCode -eq 0) {
		Add-Content -Path "passwords.txt" -Value $i
		Write-Host "FOUND!"
		break
	}
}