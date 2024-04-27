.386
.model flat,stdcall
.stack 4096
ExitProcess proto,dwExitCode:dword

.data

mynum DWORD 6h ; initialize with any value
mynum_factorial DWORD 0h 
mynum_flags WORD 0b

.code

isEven MACRO mynum
    mov edx, 0
    mov eax, mynum
    mov ebx, 2
    idiv ebx
    endm

    Factorial proc
        push ebp
        mov ebp, esp
        cmp mynum, -1
        jle badFac
        cmp mynum, 0
        je retZero
        imul edx, ecx
        sub ecx, 1
        cmp ecx, 0
        je endFac
        call Factorial
        
        endFac:
            pop ebp
            ret
    Factorial ENDP

    isPrime proc
        push ebp
        mov ebp, esp
        mov ecx, mynum
        mov ebx, 2
        cmp ecx, -1
        jle badFac
        cmp ecx, 0
        je retZero
        cmp ecx, 1
        je foundPrime
        cmp ecx, 2
        je foundPrime

        findRemZ:
            mov eax, mynum
            mov edx, 0
            cmp ebx, eax
            je foundPrime
            idiv ebx
            cmp edx, 0
            je noPrimeFound
            add ebx, 1
            cmp ecx, 0
            jle noPrimeFound
            loop findRemZ
        
        foundPrime:
            mov eax, 0
            or mynum_flags, 00000001b
            pop ebp
            ret

        noPrimeFound:
           pop ebp
           ret
        pop ebp
        ret
    isPrime endp

    main proc
    mov eax, 1
    mov edx, 1
    mov ecx, mynum
    call Factorial
    mov mynum_factorial, edx
    cmp eax, 0
    jge moveOn

    moveOn:
        call isPrime
        cmp mynum, 0
        jl ending

        keepGoing:
        cmp mynum, 0
        je ending
        isEven mynum
        cmp edx, 0
        je EvenSteven

        ending:
        mov eax, 0
        mov ax, mynum_flags ; display flags
        mov ebx, mynum_Factorial ; display factorial value

        invoke ExitProcess,0 
   
    main endp
    badFac:
       mov mynum_Factorial, -1
       pop ebp
       ret
    retZero:
       mov edx, 1
       pop ebp
       ret
    EvenSteven:
        mov eax, 0
        or mynum_flags, 00000010b
        mov ax, mynum_flags
        mov ebx, mynum_Factorial
        invoke ExitProcess,0


end main