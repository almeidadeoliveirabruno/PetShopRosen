
namespace Petshop.Models
{
    public class Plano
    {
        public int Id { get; set; }
        public string Nome { get; set; }
        public decimal Preco { get; set; }
        public string Descricao { get; set; }
        public ICollection<Animal>? Animais { get; set; }          // animais associados ao plano
    }
}