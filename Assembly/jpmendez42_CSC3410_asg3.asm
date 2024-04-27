.386
.model flat,stdcall
.stack 4096
ExitProcess proto,dwExitCode:dword

.data

s1 BYTE "Williams"
s2 BYTE "Ronaldo"
s3 BYTE "Aniston"

stringorder WORD 0h

.code

main proc

mov esi, OFFSET s1
mov edi, OFFSET s2
mov ecx, LENGTHOF s1
mov edx, 0
repe cmpsb
jb onebig
jmp onesmall

onebig:
mov esi, OFFSET s1
mov edi, OFFSET s3
mov ecx, LENGTHOF s1
repe cmpsb
jb onebest
mov stringorder, 312h
jmp done

onesmall:
mov esi, OFFSET s3
mov edi, OFFSET s1
mov ecx, LENGTHOF s1
repe cmpsb
jb oneworst
mov stringorder, 213h
jmp done

onebest:
mov esi, OFFSET s2
mov edi, OFFSET s3
mov ecx, LENGTHOF s1
repe cmpsb
jb easy
mov stringorder, 132h
jmp done

oneworst:
mov esi, OFFSET s3
mov edi, OFFSET s2
mov ecx, LENGTHOF s1
repe cmpsb
jb reverse
mov stringorder, 231h
jmp done

easy:
mov stringorder, 123h
jmp done

reverse:
mov stringorder, 321h
jmp done

done:
mov eax, 0
mov ax, stringorder; check the actual value of stringorder by looking at contents in eax register
invoke ExitProcess,0

main endp


end main