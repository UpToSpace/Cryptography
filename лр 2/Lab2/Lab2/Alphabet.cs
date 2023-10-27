using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Runtime.Serialization;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Serialization;
using static System.Net.Mime.MediaTypeNames;

namespace Lab2
{
    public static class Alphabet
    {
        public static string TextReader(string path)
        {
            string str;
            using (StreamReader reader = new StreamReader(path))
            {
                str = reader.ReadToEnd().ToLower();
            }
            return str;
        }

        public static Dictionary<char, int> LettersDict(string text)
        {
            Dictionary<char, int> lettersDict = new Dictionary<char, int>();
            foreach (char c in text)
            {
                if (char.IsDigit(c) || char.IsLetter(c))
                {
                    if (!lettersDict.ContainsKey(c))
                        lettersDict.Add(c, 1);
                    else lettersDict[c]++;
                }
            }
            return lettersDict;
        }

        public static Dictionary<char, double> Probs(string text)
        {
            Dictionary<char, int> lettersDict = LettersDict(text);
            Dictionary<char, double> letters = new Dictionary<char, double>();
            for (int i = 0; i < lettersDict.Values.Count; i++)
            {
                letters.Add(lettersDict.Keys.ToArray()[i], (double)lettersDict.Values.ToArray()[i] / lettersDict.Values.Sum());
            }
            return letters;
        }

        public static double Entropy(string text)
        {
            double entropy = 0;
            Dictionary<char, double> lettersProbs = Probs(text);
            for (int i = 0; i < lettersProbs.Values.Count; i++)
            {
                entropy += lettersProbs.Values.ToArray()[i] * Math.Log(lettersProbs.Values.ToArray()[i], 2);
            }
            return -entropy;
        }

        public static string ConvertToAscii(string text)
        {
            string asciiTxt = null;
            foreach (char c in text)
            {
                if (char.IsLetter(c))
                {
                    asciiTxt += Convert.ToString(c, 2);
                }
            }
            return asciiTxt;
        }

        public static void Serialize(string path, Dictionary<char, double> probs)
        {
            File.Delete(path);
            using (FileStream fs = new FileStream(path, FileMode.OpenOrCreate))
            {
                DataContractSerializer formatter = new DataContractSerializer(typeof(Dictionary<char, double>));
                formatter.WriteObject(fs, probs);
            }
        }

        public static double QuantityOfInformation(double entropy, string text)
        {
            return entropy * text.Length;
        }

        public static double MistakeQuantity(double mistakeProb, string text, double entropy)
        {
            return text.Length * (entropy - (-mistakeProb * Math.Log(mistakeProb, 2) - (1 - mistakeProb) * Math.Log(1 - mistakeProb, 2)));
        }
    }
}