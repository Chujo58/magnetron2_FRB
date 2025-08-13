#include "MyConditionalPrior.h"
#include "DNest4/code/Utils.h"
#include "Data.h"
#include "gsl/gsl/gsl_cdf.h"
#include <cmath>

using namespace DNest4;

MyConditionalPrior::MyConditionalPrior(double x_min, double x_max, 
					double mu_min, double mu_max)
:x_min(x_min)
,x_max(x_max)
,mu_min(mu_min)
,mu_max(mu_max)
,min_width(0.)
{

}

void MyConditionalPrior::from_prior(RNG& rng)
{
	mu = tan(M_PI*(0.97*rng.rand() - 0.485)); //log (mu) is Cauchy so mu is exp(log(mu))
	mu = exp(mu);
	mu_widths = exp(log(1E-3*(x_max - x_min)) + log(1E3)*rng.rand());

	sig = 2.*rng.rand();
	sig_widths = 2.*rng.rand();


	a = -10. + 20.*rng.rand();
	b = 5.*rng.rand();
}

double MyConditionalPrior::perturb_hyperparameters(RNG& rng)
{
	double logH = 0.;

	int which = rng.rand_int(6);

	if(which == 0)
	{
		mu = log(mu);
		mu = (atan(mu)/M_PI + 0.485)/0.97;
		mu += pow(10., 1.5 - 6.*rng.rand())*rng.randn();
		mu = mod(mu, 1.);
		mu = tan(M_PI*(0.97*mu - 0.485));
		mu = exp(mu);
	}
	if(which == 1)
	{
		mu_widths = log(mu_widths/(x_max - x_min));
		mu_widths += log(1E3)*pow(10., 1.5 - 6.*rng.rand())*rng.randn();
		mu_widths = mod(mu_widths - log(1E-3), log(1E3)) + log(1E-3);
		mu_widths = (x_max - x_min)*exp(mu_widths);
	}
	if(which == 2)
	{
		sig += 2.*rng.randh();
		sig = mod(sig, 2.);
	}
	if(which == 3)
	{
		sig_widths += 2.*rng.randh();
		sig_widths = mod(sig, 2.);
	}
        if(which == 4)
	{
		a += 20.*rng.randh();
		a = mod(a + 10., 20.) - 10.;
	}
	if(which == 5)
	{
		b += 5.*rng.randh();
		b = mod(b, 5.);
	}

	return logH;
}

// vec[0] = ToA; vec[1] = amplitude; vec[2] = rise; vec[3] = skew
double MyConditionalPrior::log_pdf(const std::vector<double>& vec) const
{
	if(vec[0] < x_min || vec[0] > x_max || vec[1] < 0.0 || vec[2] < min_width
		|| log(vec[3]) < (a-b) || log(vec[3]) > (a + b))
		return -1E300;

	return -log(mu) - vec[1]/mu - log(mu_widths)
			- (vec[2] - min_width)/mu_widths - log(2.*b*vec[3]);
}

void MyConditionalPrior::from_uniform(std::vector<double>& vec) const
{
	vec[0] = x_min + (x_max - x_min)*vec[0]; // ToA is uniform in [x_min, x_max]
	vec[1] = exp(log(mu) + sig*gsl_cdf_ugaussian_Pinv(vec[1])); // Amplitude is log-normal
	vec[2] = exp(log(mu_widths) + sig_widths*gsl_cdf_ugaussian_Pinv(vec[2])); // Rise is log-normal
	vec[3] = exp(a - b + 2.*b*vec[3]); // Skew is uniform in [a-b, a+b]. a is the mean of the uniform distribution and b is the scale.
}

void MyConditionalPrior::to_uniform(std::vector<double>& vec) const
{
	vec[0] = (vec[0] - x_min)/(x_max - x_min);
	vec[1] = gsl_cdf_ugaussian_P((log(vec[1]) - log(mu))/sig);
	vec[2] = gsl_cdf_ugaussian_P((log(vec[2]) - log(mu_widths))/sig_widths);
	vec[3] = (log(vec[3]) + b - a)/(2.*b);
}

void MyConditionalPrior::print(std::ostream& out) const
{
//	out<<mu<<' '<<mu_widths<<' '<<a<<' '<<b<<' ';
	out<<mu<<' '<<sig<<' '<<mu_widths<<' '<<sig_widths<<' '<<a<<' '<<b<<' ';

}

