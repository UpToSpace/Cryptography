using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Lab2
{
    internal class Program
    {
        static void Main(string[] args)
        {
            double frEntropy = 0, belEntropy = 0, binEntropy = 0;

            Console.WriteLine("Рассчитать энтропию алфавитов: один – на латинице, другой – на кириллице \n");
            frEntropy = Alphabet.Entropy(Alphabet.TextReader(@"D:\University\крипта\лр 2\Lab2\french.txt"));
            Console.WriteLine("Энтропия французского: " + frEntropy);
            belEntropy = Alphabet.Entropy(Alphabet.TextReader(@"D:\University\крипта\лр 2\Lab2\belarusian.txt"));
            Console.WriteLine("Энтропия беларуского: " + belEntropy);

            //частоты появления символов алфавитов оформить в виде гистограмм
            Alphabet.Serialize(@"D:\University\крипта\лр 2\Lab2\probs_fr.xml", Alphabet.Probs(Alphabet.TextReader(@"D:\University\крипта\лр 2\Lab2\french.txt")));
            Alphabet.Serialize(@"D:\University\крипта\лр 2\Lab2\probs_bel.xml", Alphabet.Probs(Alphabet.TextReader(@"D:\University\крипта\лр 2\Lab2\belarusian.txt")));
            //б) определить энтропию бинарного алфавита
            Console.WriteLine("\nДля входных документов, представленных в бинарных кодах, определить энтропию бинарного алфавита \n");
            binEntropy = Alphabet.Entropy(Alphabet.ConvertToAscii(Alphabet.TextReader(@"D:\University\крипта\лр 2\Lab2\french.txt")));
            Console.WriteLine("Энтропия бинарного для документа на французском: " + binEntropy);
            Console.WriteLine("Энтропия бинарного для документа на беларуском: " + Alphabet.Entropy(Alphabet.ConvertToAscii(Alphabet.TextReader(@"D:\University\крипта\лр 2\Lab2\belarusian.txt"))));
            //в) подсчитать кол-во информации в ФИО на исх. алфавите и кодах ASCII
            Console.WriteLine("\nПодсчитать количество информации в сообщении, состоящем из собственных фамилии, имени и отчества\n");
            Console.WriteLine("Количество информации на французском: " + Alphabet.QuantityOfInformation(frEntropy, "Korzhova Valeria Sergeevna"));
            Console.WriteLine("Количество информации на беларуском: " + Alphabet.QuantityOfInformation(belEntropy, "Каржова Валерыя Сяргееўна"));
            Console.WriteLine("Количество информации в ASCII: " + Alphabet.QuantityOfInformation(binEntropy, Alphabet.ConvertToAscii("Korzhova Valeria Sergeevna")));
            //г) вероятность 0,1
            Console.WriteLine("\nПри условии, что вероятность ошибочной передачи единичного бита сообщения составляет\n");
            Console.WriteLine("Количество информации на французском с вероятностью 0,1: " + Alphabet.MistakeQuantity(0.1, "Korzhova Valeria Sergeevna", frEntropy));
            Console.WriteLine("Количество информации на беларуском с вероятностью 0,1: " + Alphabet.MistakeQuantity(0.1, "Каржова Валерыя Сяргееўна", belEntropy));
            Console.WriteLine("Количество информации в ASCII с вероятностью 0,1: " + Alphabet.MistakeQuantity(0.1, Alphabet.ConvertToAscii("Korzhova Valeria Sergeevna"), binEntropy));
            //вероятность 0,5
            Console.WriteLine("\nКоличество информации на французском с вероятностью 0,5: " + Alphabet.MistakeQuantity(0.5, "Korzhova Valeria Sergeevna", 1));
            Console.WriteLine("Количество информации на беларуском с вероятностью 0,5: " + Alphabet.MistakeQuantity(0.5, "Каржова Валерыя Сяргееўна", 1));
            Console.WriteLine("Количество информации в ASCII с вероятностью 0,5: " + Alphabet.MistakeQuantity(0.5, Alphabet.ConvertToAscii("Korzhova Valeria Sergeevna"), 1));
            //вероятность 1,0
            Console.WriteLine("\nКоличество информации на французском с вероятностью 1,0: " + Alphabet.MistakeQuantity(0.999, "Korzhova Valeria Sergeevna", frEntropy));
            Console.WriteLine("Количество информации на беларуском с вероятностью 1,0: " + Alphabet.MistakeQuantity(0.999, "Каржова Валерыя Сяргееўна", belEntropy));
            Console.WriteLine("Количество информации в ASCII с вероятностью 1,0: " + Alphabet.MistakeQuantity(0.999, Alphabet.ConvertToAscii("Korzhova Valeria Sergeevna"), binEntropy));
            Console.ReadLine();
        }
    }
}
