@echo off
REM ============================================================
REM  ANTIGRAVITY MODEL BENCHMARK — quick CPU throughput check
REM  Compare semua profile (fast/balanced/coder/task)
REM  Kasih angka tok/s + waktu first-token + total
REM ============================================================
setlocal enabledelayedexpansion

set "OLLAMA_HOST_LOCAL=http://127.0.0.1:11434"
set "PROMPT_SHORT=Sebutkan 5 ibukota provinsi di Pulau Sumatra. Format daftar."
set "PROMPT_LONG=Tulis fungsi Python untuk hitung Fibonacci dengan memoization, sertakan docstring dan 1 contoh penggunaan."

echo.
echo ============================================================
echo   ANTIGRAVITY BENCHMARK (CPU-only)
echo   Prompt SHORT (~80 tok output) ^| Prompt LONG (~250 tok output)
echo ============================================================
echo.

call :bench antigravity-fast       "%PROMPT_SHORT%"  120
call :bench antigravity-balanced   "%PROMPT_SHORT%"  150
call :bench antigravity-coder      "%PROMPT_LONG%"   400
call :bench antigravity-task       "%PROMPT_SHORT%"  60
call :bench qwen2.5:3b             "%PROMPT_SHORT%"  150
call :bench llama3.1:8b            "%PROMPT_SHORT%"  150

echo.
echo ============================================================
echo   Done. Pakai profile dengan tok/s tertinggi yang masih
echo   memenuhi kualitas yang kamu butuhkan.
echo ============================================================
endlocal
exit /b 0


:bench
set "MODEL=%~1"
set "PROMPT=%~2"
set "MAXTOK=%~3"
echo === %MODEL% ===
powershell -NoProfile -Command "$body = @{ model='%MODEL%'; prompt='%PROMPT%'; stream=$false; options=@{num_predict=%MAXTOK%} } | ConvertTo-Json; try { $r = Invoke-RestMethod -Method POST -Uri '%OLLAMA_HOST_LOCAL%/api/generate' -Body $body -ContentType 'application/json' -TimeoutSec 600; $tok = $r.eval_count; $eDur = $r.eval_duration/1e9; $pDur = $r.prompt_eval_duration/1e9; $loadDur = $r.load_duration/1e9; $tps = if($eDur -gt 0){[math]::Round($tok/$eDur,2)}else{0}; Write-Host ('  load:        ' + [math]::Round($loadDur,2) + 's'); Write-Host ('  prompt-eval: ' + [math]::Round($pDur,2) + 's'); Write-Host ('  generate:    ' + $tok + ' tok in ' + [math]::Round($eDur,2) + 's = ' + $tps + ' tok/s'); } catch { Write-Host ('  ERROR: ' + $_.Exception.Message) }"
echo.
goto :eof
