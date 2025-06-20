# Quick test to intercept input
break wgetch
commands
silent
# Always return 'w' (up)
return 119
continue
end
run
