using Microsoft.EntityFrameworkCore;
using Petshop.Models;

namespace Petshop.Data
{
    public class PetshopContext : DbContext
    {
        public PetshopContext(DbContextOptions<PetshopContext> options)
           : base(options) { }

        public DbSet<Cliente> Clientes { get; set; }
        public DbSet<Animal> Animais { get; set; }
        public DbSet<Plano> Planos { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Define a precisão da coluna Preco na tabela Plano
            modelBuilder.Entity<Plano>()
                .Property(p => p.Preco)
                .HasPrecision(10, 2);
        }
    }
}
