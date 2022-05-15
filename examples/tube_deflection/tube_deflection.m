args = argv();
input_matfile = args{1};
output_file = args{2};
inputs = load(input_matfile);

F = double(getfield(inputs, 'F'));
L = double(getfield(inputs, 'L'));
a = double(getfield(inputs, 'a'));
D = double(getfield(inputs, 'D'));
d = double(getfield(inputs, 'd'));
E = double(getfield(inputs, 'E'));

b = L - a;
I = pi * (D .^ 4 - d .^ 4) / 32.0;
g1 = -F * ((a .^ 2 * (L - a) .^ 2) / (3.0 * E * L * I));
g2 = -F * ((b * (L .^ 2 - b .^ 2)) / (6.0 * E * L * I));
g3 =  F * ((a * (L .^ 2 - a .^ 2)) / (6.0 * E * L * I));

save("-mat4-binary", output_file, "g1", "g2", "g3");

