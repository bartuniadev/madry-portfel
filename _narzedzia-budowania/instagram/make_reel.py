# usage: python3 make_reel.py <karuzele_dir> <set> <n_slides> <out.mp4>
import subprocess, sys
kdir, name, n, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
hold, fade = 3.2, 0.5
args = ['ffmpeg', '-y', '-loglevel', 'error']
for i in range(1, n + 1):
    d = hold + fade + (1.5 if i == n else 0)
    args += ['-loop', '1', '-t', f'{d}', '-i', f'{kdir}/{name}-{i}.png']
f = []
for i in range(n):
    f.append(f'[{i}:v]scale=1080:1920,setsar=1,fps=30,format=yuv420p[v{i}]')
prev = 'v0'
for i in range(1, n):
    off = round(i * hold, 3)
    f.append(f'[{prev}][v{i}]xfade=transition=slideleft:duration={fade}:offset={off}[x{i}]')
    prev = f'x{i}'
args += ['-filter_complex', ';'.join(f), '-map', f'[{prev}]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '22', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out]
subprocess.run(args, check=True)
print(out)
