from subprocess import call
import os


class BoolSimModel:
    def __init__(self, model_name):
        self._model_name = model_name
        self._base_name = "_".join( model_name.split(".")[:-1] )
        self._attractors = None

    def attractors(self):
        if self._attractors is None:
            output_pattern = f"{self._base_name}_attractor"
            command = ("boolSim", '-t', '-f', self._model_name, '-p', '3', '-o', output_pattern)
            call( command  )

            self._attractors = []
            i = 1
            while True:
                cur_attractor = f"{output_pattern}_{i}.txt"
                if not os.path.exists(cur_attractor): break
                self._attractors.append( BoolSimStates(cur_attractor))
                i += 1

        return self._attractors


    def reachable(self, initial, output=None, suffix="reach", max_steps=None):
        if output is None:
            output = f"{initial.statefile[:-4]}_{suffix}.txt"
        command = [ "boolSim", '-t', '-f', self._model_name, '-p', '3', '-i', initial.statefile, '-o', output ]
        if max_steps is not None:
            command += [ '-n', str(max_steps) ]
        call( command )
        return BoolSimStates(output)


class BoolSimStates:
    def __init__(self, statefile):
        self.statefile = statefile
        self._count = None

    def exclude(self, output, excluded):
        excluded = [ e.statefile for e in excluded ]
        command = ["boolSim_setutils", '-t', 'difference', self.statefile, '-o', output ] + excluded
        call( command )
        return BoolSimStates( output )

    def intersect(self, output, other):
        command = ["boolSim_setutils", '-t', 'intersection', self.statefile, '-o', output, other.statefile ]
        call( command )
        return BoolSimStates( output )
    
    def count(self):
        if self._count is None:
            self._count = 0
            with open(self.statefile) as f:
                f.readline()
                for line in f:
                    cur = 1
                    for c in line:
                        if c == "2": cur *= 2
                    self._count += cur
        
        return self._count
    
    def show(self):
        with open(self.statefile) as f:
            for line in f: print(line.replace("2", "-"), end="")
        print()
    
    def simplify(self):
        # Load the boolsim state file and save it in the espresso format
        with open(self.statefile) as f:
            f_lines = f.readlines()

        f_espresso = f"{self.statefile}.espresso"
        f_simplified = f"{self.statefile}_simplified.espresso"
        nodes = f_lines[0].rstrip().split(' ')
        with open(f_espresso, 'w') as fh:
            fh.write(".i " + str(len(nodes)) + "\n.o 1\n")
            for line in f_lines[1:]:
                line = "".join( line.rstrip().split(' ') )
                fh.write(line.replace("2", "-"))
                fh.write(" 1\n");
            fh.write(".e")

        # simplify with espresso
        with open(f_simplified, 'w') as fh:
            call( [ "espresso", f_espresso ], stdout=fh )
            
        # Parse the espresso output to get user-readable patterns
        with open(f_simplified) as f:
            f_lines = f.readlines()

        f_simplified = f"{self.statefile[:-4]}_simplified.txt"
        with open(f_simplified, 'w') as fh:
            fh.write(' '.join(nodes) + "\n")
            for line in f_lines[3:-1]:
                line = line[:-3].replace("-","2")
                fh.write(' '.join( [c for c in line] ) + "\n")
        
        return BoolSimStates(f_simplified)

