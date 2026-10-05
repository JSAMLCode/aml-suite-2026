import subprocess,sys
def sheet(d,times,cols,w,outp):
    args=[];fc=""
    for i,t in enumerate(times):
        args+=["-i",f"{d}/t{t}.png"];fc+=f"[{i}]scale={w}:-1[s{i}];"
    rows=[]
    for r in range(0,len(times),cols):
        n=min(cols,len(times)-r);ids="".join(f"[s{i}]" for i in range(r,r+n))
        fc+=f"{ids}hstack=inputs={n}[r{r}];" if n>1 else f"{ids}null[r{r}];";rows.append(f"[r{r}]")
    fc+="".join(rows)+(f"vstack=inputs={len(rows)}" if len(rows)>1 else "null")
    subprocess.run(["ffmpeg","-loglevel","error","-y",*args,"-filter_complex",fc,outp],check=True)
T=['0.30','1.20','2.20','3.15','3.90','4.95','5.10','6.20','7.00','8.00','9.00','10.30','11.10','11.70','12.20','12.80','13.20','14.20']
if 'h' in sys.argv: sheet('test_h',T[:9],3,640,'sh1.png');sheet('test_h',T[9:],3,640,'sh2.png')
if 'v' in sys.argv: sheet('test_v',T[:9],9,240,'sv1.png');sheet('test_v',T[9:],9,240,'sv2.png')
