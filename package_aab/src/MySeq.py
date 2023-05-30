import re


class MySeq:
    """
    Class presenting the methods that allow the manipulation of DNA, RNA and protein sequences.
    """

    def __init__(self, seq: str, seq_type: str) -> None:
        """
        Method that keeps the values from the rest of the methods.
        :param seq: sequence introduced
        :param seq_type: type of sequence introduced
        """
        self.seq = seq.upper()
        self.seq_type = seq_type

    def __len__(self) -> int:
        """
        Method that returns the length of the sequence introduced.
        :return: length of the sequence introduced
        """
        return len(self.seq)

    def __getslice__(self, i: int, j: int) -> str:
        """
        Method that slices the sequence between i and j.
        :param i: Start position
        :param j: End position
        :return:  String with the slice of the sequence
        """
        return self.seq[i:j]

    def __getitem__(self, n: int) -> str:
        """
        Method that allows returning an item from the indexing of an instance.
        :param n: position of n.
        :return:
        """
        return self.seq[n]

    def __repr__(self) -> str:
        """
        Method that represent the objects of the class as strings.
        :return: objects as strings.
        """
        return str(self.seq)

    def printSeq(self):
        """
        Method that prints the complete sequence
        :return: string of the complete sequence
        """
        print(self.seq)

    def alphabet(self):
        """
        Method that verifies the type of sequence
        :return: returns the possible characters of the sequence.
        """
        if self.seq_type == "dna":
            return "ACGT"
        elif self.seq_type == "rna":
            return "ACGU"
        elif self.seq_type == "protein":
            return "ACDEFGHIKLMNPQRSTVWY"
        else:
            return None

    def valida(self):
        """
        Method that checks if all the characters in sequence are present in the alphabet defined
        :return:
        """
        alf = self.alphabet()   # obtain the alphabet
        res = True
        i = 0  # initialize the counter
        while i < len(self.seq) and res:
            if self.seq[i] not in alf:  # check if the current character is not in the alphabet
                res = False
            else:
                # if it's in the alphabet, move to the next character
                i += 1
        return res

    def validateSeqRE(self) -> bool:
        """
        Method that validates the sequence according to the type of characters present through regular expressions.
        :return: value True or False if the sequences are valid or invalid, respectively
        """
        if self.seq_type == "dna":
            if re.search("[^ACTGactg]", self.seq) != None:
                return False
            else:
                return True
        elif self.seq_type == "rna":
            if re.search("[^ACUGacug]", self.seq) != None:
                return False
            else:
                return True
        elif self.seq_type == "protein":
            if re.search("[^ACDEFGHIKLMNPQRSTVWY_acdefghiklmnpqrstvwy]", self.seq) != None:
                return False
            else:
                return True
        else:
            return False

    def transcription(self):
        """
        Method that returns the transcript sequence. Replacing of the thymine base 'T' for the uracil base 'U'
        Only executes in case the object is a DNA sequence
        :return: RNA sequence
        """
        if self.seq_type == "dna":  # if the sequence if the type of dna
            return MySeq(self.seq.upper().replace("T", "U"), "rna")  # replace "T" for "U"
        else:
            return None

    def reverseComplement(self):
        """
        Method that inverts and complements the sequence
        Only executes in case the object is a DNA sequence
        :return: DNA sequence
        """
        if (self.seq_type != "dna"):
            return None
        else:
            self.seq = self.seq[::-1].lower()
            inv_comp = self.seq.replace("a", "T").replace("g", "C").replace("c", "G").replace("t", "A")
        return MySeq(inv_comp, "dna")

    def rnaCodon(self) -> list:
        """
        Method that searches for the codons in the sequence.
        :returns: list of codons
        """
        codon = re.findall(r'...', self.seq)
        return codon

    def seqTranslation(self, initial_pos: int = 0):
        """
        Method that performs the translation of the sequence
        :param initial_pos: determines the initial position of the reading sequence
        :return:
        """
        if (self.seq_type != "dna"):  # verifies if the sequence is type dna
            return None
        seq = self.seq.upper()
        seq_amino = ""  # initiate the empty string
        for pos in range(initial_pos, len(seq) - 2, 3):  # read each caracter of the position
            # inicia na posição inicial e para dois nucleótidos antes do final da sequência,
            # de forma a ler o último codão inteiro
            # incrementes 3 nucl (codons)
            codon = seq[pos:pos+3]  # read codons
            seq_amino += self.codonTranslate(codon)  # add the protein correspondent to the codon
        return MySeq(seq_amino, "protein")

    def orfs(self):
        """
        Method that determines the open reading frames (ORF), i.e. the sequences between the initiation codon
        and the STOP codon. It generates six reading frames of the DNA sequence and the reverse complement.
        :return: returns ORF's
        """
        if (self.seq_type != "dna"):
            return None
        frames = []
        frames.append(self.seqTranslation(0)) # starts reading of the frame in the first position
        frames.append(self.seqTranslation(1)) # starts reading of the frame in the second position
        frames.append(self.seqTranslation(2)) # starts reading of the frame in the third position
        inv_comp = self.reverseComplement() #determina o complemento inverso
        frames.append(inv_comp.seqTranslation(0)) # starts reading of the frame in the last position
        frames.append(inv_comp.seqTranslation(1)) # starts reading of the frame in the penúltima posição
        frames.append(inv_comp.seqTranslation(2)) # starts reading of the frame in the antepenúltima posição
        return frames

    def codonTranslate(self, cod: str) -> str:
        """
        Method that translates codons into their respective amino acids.
        :param cod: codon to look for in the codon table
        :return: amino acid sequence
        """
        codon_table = {"GCT": "A", "GCA": "A", "GCC": "A", "TGT": "C", "TGC": "C",
              "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E", "TTT": "F", "TTC": "F",
              "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G", "CAT": "H", "CAC": "H",
              "ATA": "I", "ATT": "I", "ATC": "I",
              "AAA": "K", "AAG": "K",
              "TTA": "L", "TTG": "L", "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
              "ATG": "M", "AAT": "N", "AAC": "N",
              "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
              "CAA": "Q", "CAG": "Q",
              "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R", "AGA": "R", "AGG": "R",
              "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S", "AGT": "S", "AGC": "S",
              "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
              "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
              "TGG": "W",
              "TAT": "Y", "TAC": "Y",
              "TAA": "_", "TAG": "_", "TGA": "_"} #dicionário em que as chaves são os codões e os valores os aminoácidos
        if cod in codon_table:
            amin = codon_table[cod] #guarda o aminoácido correspondente ao codão
        else:
            amin = "X"  #marca erros de procura com um X
        return amin

    def longestProteinSeq(self):
        """
        Method searching for the longest protein sequence
        :return: longest proteic sequence
        """
        if (self.seq_type != "prot"): #determina se o tipo de sequência é uma proteína
            return None
        seq_amin = self.seq.upper()
        current_prot = "" #string vazia para guardar a sequência que está a ser lida
        longest_prot = "" #string vazia para guardar a sequência da maior proteina
        for aa in seq_amin: #lê cada aminoácido na sequência
            if aa == "_": #verifica se é um codão stop
                if len(current_prot) > len(longest_prot): #verifica se a proteína que está a ser lida é superior
                    #à última proteina gaurdada na lista de maior proteínas
                    longest_prot = current_prot #se for, guarda a proteína atual como a mais longa
                current_prot = "" #volta a zerar a lista de proteínas atuais
            else:
                if len(current_prot) > 0 or aa == "M": #verifica se a proteina tem um cumprimento superior a zero
                    #e começa a ler se o aminoácido for uma metionina.
                    current_prot += aa #adiciona o aminoácido à lista
        return MySeq(longest_prot, "protein")

    def allProtein(self):
        """
        Method that constructs of a list with all the existing and possible proteins in the sequence. The sequence can be proteic or DNA
        Only executes in case the object is a DNA or AMINO sequence
        :return: DNA or amino sequence
        """
        if (self.seq_type != "prot"):  # verifica se a sequência é uma proteína
            return None
        seq_aa = self.seq.upper()
        current_prot = []  # lista da proteína a ser lida
        prot_list = []  # lista de proteínas totais
        for aa in seq_aa:  # lê os aminoácidos da sequência
            if aa == "_":  # verifica se é um codão stop
                if current_prot:
                    for p in current_prot:
                        prot_list.append(MySeq(p, "protein")) # adiciona as proteínas lidas na lista de proteínas totais
                    current_prot = [] # zera a lista de proteínas lidas
            else:
                if aa == "M": # verifica se é um codão de iniciação
                    current_prot.append("")
                for i in range(len(current_prot)):
                    current_prot[i] += aa # adiciona os aminoácidos à lista
        return prot_list

    def largestOrfProtein(self):
        """
        Method to get the bigger protein in the sequence
        :return: string with the bigger protein
        """
        if (self.seq_type != "prot"): # verifica se a sequência é do tipo proteina
            return None
        larg_prot = MySeq("", "prot")
        for orf in self.orfs(): # lê as ORF
            prot = orf.largestOrfProtein() # define as ORF como proteinas
            if len(prot.seq) > len(larg_prot.seq): # verifica se a proteina a ler tem um comprimento superior
                # à maior proteina.
                larg_prot = prot # se sim, define a proteina como a maior proteina
        return larg_prot
